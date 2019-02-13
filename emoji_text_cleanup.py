import logging
import emoji
import re

class EmojiTextCleaner():

    def __init__(self):
        pass

    def is_emoji(self, char):
        if char in emoji.UNICODE_EMOJI:
            return True
        return False

    def clean_text(self, line):
        cleaned_line = ""

        for char in line:
            if self.is_emoji(char):
                cleaned_line += " " + char + " "
            else:
                cleaned_line += char

        return cleaned_line

    def main(self):
        clean_text = open('emojipasta_clean_multiples.txt', 'a')
        with open('emojipasta_raw.txt', 'r') as raw_text:
            line = raw_text.readline()
            while line:
                line = self.clean_text(line)
                is_end_of_line = False
                end_of_line_index = len(line)
                index = 0

                while not is_end_of_line:
                    char = line[index]
                    is_emoji_text = False

                    ## Get Emoji labels
                    if self.is_emoji(char):
                        is_emoji_text = True
                        cleaned_label_with_text = ""
                        emoji_index = index
                        is_emoji_block = True
                        emoji_count = 0
                        emoji_labels = "__label__"
                        next_char = ""

                        ## Get emoji labels
                        while is_emoji_block:
                            if self.is_emoji(line[emoji_index]):
                                emoji_count += 1
                                emoji_labels += line[emoji_index]

                            next_char = line[emoji_index + 1]

                            if next_char == " ":
                                emoji_index += 1
                            elif not self.is_emoji(next_char):
                                is_emoji_block = False
                            else:
                                emoji_index += 1

                        emoji_labels += " "

                        ## Get text to attatch to emoji labels
                        text_index = index - 1
                        is_text_block = True
                        has_seen_space = False
                        text = ""

                        while is_text_block:
                            if line[text_index] == " ":
                                if has_seen_space:
                                    break
                                text_index -= 1
                                continue
                            elif self.is_emoji(line[text_index]):
                                is_text_block = False
                                break
                            elif not line[text_index].isalpha() and not line[text_index] == "'":
                                is_text_block = False
                                break
                            else:
                                has_seen_space = True
                                text = line[text_index] + text
                                text_index -= 1

                        text = text.strip()

                        if text and emoji_count > 1:
                            clean_text.write(emoji_labels + text + "\n")

                        index = emoji_index ## Skip characters that we know are have been parsed

                    else:
                        index += 1

                    if index >= end_of_line_index:
                        is_end_of_line = True

                line = raw_text.readline()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    emojiTextCleaner = EmojiTextCleaner()
    emojiTextCleaner.main()
