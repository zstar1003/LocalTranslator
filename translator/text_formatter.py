"""
文本格式保持模块
用于在翻译前后保持文本的排版格式
"""

import re
from typing import List, Tuple


class TextFormatter:
    """文本格式保持器，用于在翻译前后保持文本排版"""

    def __init__(self):
        # 存储原始格式信息
        self.format_info = {
            "paragraph_breaks": [],
            "line_breaks": [],
            "leading_spaces": [],
            "trailing_spaces": [],
        }

    def extract_format(self, text: str) -> str:
        """
        提取文本中的格式信息，返回纯文本
        使用简化的方法，只保留基本的段落和行结构

        Args:
            text: 原始文本

        Returns:
            str: 处理后的纯文本
        """
        # 重置格式信息
        self.format_info = {
            "paragraph_breaks": [],
            "line_breaks": [],
            "leading_spaces": [],
            "trailing_spaces": [],
        }

        # 分割成行来处理
        lines = text.split("\n")
        processed_lines = []

        for i, line in enumerate(lines):
            # 记录每行的前导空格
            leading_match = re.match(r"^(\s*)", line)
            leading_spaces = leading_match.group(1) if leading_match else ""
            self.format_info["leading_spaces"].append(leading_spaces)

            # 记录每行的尾随空格
            trailing_match = re.search(r"(\s*)$", line)
            trailing_spaces = trailing_match.group(1) if trailing_match else ""
            self.format_info["trailing_spaces"].append(trailing_spaces)

            # 去除前导和尾随空格，保留内容
            clean_line = line.strip()
            processed_lines.append(clean_line)

        # 记录段落分隔（空行）
        for i, line in enumerate(processed_lines):
            if line == "":
                self.format_info["paragraph_breaks"].append(i)

        # 保存原始行结构，用于后续恢复
        self.format_info["original_structure"] = lines

        # 返回清理后的文本，用单个空格分隔非空行
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        return " ".join(non_empty_lines)

    def restore_format(self, translated_text: str) -> str:
        """
        将格式信息恢复到翻译后的文本中
        使用简化的方法，基于原始文本的行结构重新格式化

        Args:
            translated_text: 翻译后的文本

        Returns:
            str: 恢复格式后的文本
        """
        return self._simple_restore_format(translated_text)

    def _simple_restore_format(self, translated_text: str) -> str:
        """
        简单的格式恢复，基于原始行结构
        """
        if not self.format_info or not self.format_info.get("original_structure"):
            return translated_text

        original_lines = self.format_info["original_structure"]

        # 获取非空的原始行，用于匹配翻译内容
        non_empty_original_lines = [line for line in original_lines if line.strip()]

        # 更智能的分割翻译文本
        translated_parts = self._split_translation_by_structure(
            translated_text, non_empty_original_lines
        )

        # 重新构建格式
        result_lines = []
        part_index = 0

        for original_line in original_lines:
            if not original_line.strip():
                # 保持空行
                result_lines.append("")
            elif part_index < len(translated_parts):
                # 保持原始缩进
                leading_spaces = len(original_line) - len(original_line.lstrip())
                indent = " " * leading_spaces
                result_lines.append(indent + translated_parts[part_index])
                part_index += 1
            else:
                # 如果翻译内容用完了，尝试翻译剩余的原始行
                stripped_original = original_line.strip()
                leading_spaces = len(original_line) - len(original_line.lstrip())
                indent = " " * leading_spaces

                # 对于简单的标签行，尝试简单翻译
                if stripped_original.startswith(("Error:", "Source:", "Original:")):
                    translated_label = self._translate_simple_label(stripped_original)
                    result_lines.append(indent + translated_label)
                else:
                    result_lines.append(original_line)

        return "\n".join(result_lines)

    def _split_translation_by_structure(
        self, translated_text: str, original_lines: list
    ) -> list:
        """
        根据原始结构智能分割翻译文本
        """
        target_count = len(original_lines)

        # 首先尝试按句号等强分隔符分割
        strong_splits = re.split(r"([.。]\s*)", translated_text)
        sentences = []
        for i in range(0, len(strong_splits), 2):
            if i + 1 < len(strong_splits):
                sentence = (strong_splits[i] + strong_splits[i + 1]).strip()
                if sentence:
                    sentences.append(sentence)
            elif strong_splits[i].strip():
                sentences.append(strong_splits[i].strip())

        # 如果句子数量不够，尝试按其他标点分割
        if len(sentences) < target_count:
            # 尝试按逗号、分号等分割
            all_parts = []
            for sentence in sentences:
                parts = re.split(r"([,，;；]\s*)", sentence)
                current_part = ""
                for i, part in enumerate(parts):
                    current_part += part
                    if i % 2 == 1 or i == len(parts) - 1:  # 分隔符后或最后一部分
                        if current_part.strip():
                            all_parts.append(current_part.strip())
                        current_part = ""

            if len(all_parts) >= target_count:
                return all_parts[:target_count]

        # 如果还是不够，按空格平均分割
        if len(sentences) < target_count:
            words = translated_text.split()
            words_per_part = max(1, len(words) // target_count)
            parts = []
            for i in range(0, len(words), words_per_part):
                part = " ".join(words[i : i + words_per_part])
                if part.strip():
                    parts.append(part.strip())
            return parts[:target_count]

        return sentences[:target_count]

    def _translate_simple_label(self, text: str) -> str:
        """
        简单翻译标签行
        """
        if text.startswith("Error:"):
            return text.replace("Error:", "错误:")
        elif text.startswith("Source:"):
            return text.replace("Source:", "来源:")
        elif text.startswith("Original:"):
            return text.replace("Original:", "原件:")
        else:
            return text

    def process_translation(self, original_text: str, translated_text: str) -> str:
        """
        完整的格式保持处理流程

        Args:
            original_text: 原始文本
            translated_text: 翻译后的文本

        Returns:
            str: 格式化后的翻译文本
        """
        # 提取原始文本的格式
        clean_text = self.extract_format(original_text)

        # 恢复格式到翻译文本
        formatted_translation = self.restore_format(translated_text)

        return formatted_translation
