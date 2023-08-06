#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Highlight the Portion of the Output Text that corresponds to the User Input Text """


from baseblock import TextUtils
from baseblock import BaseObject

from fast_sentence_tokenize import tokenize_text


class HighlightOutputText(BaseObject):
    """ Highlight the Portion of the Output Text that corresponds to the User Input Text """

    def __init__(self):
        """ Change Log

        Created:
            6-Oct-2022
            craigtrim@gmail.com
            *   GRAFFL-CORE-0004
        Updated:
            12-Oct-2022
            craigtrim@gmail.com
            *   ported from owl-parser in pursuit of
                https://github.com/craigtrim/climate-bot/issues/8
        Updated:
            29-Oct-2022
            craigtrim@gmail.com
            *   ported from 'climate-bot' and renamed from 'output-text-highlighter'
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                text_1: str,
                text_2: str) -> str:

        tokens_1 = tokenize_text(text_1.lower())
        tokens_2 = tokenize_text(text_2.lower())

        common_tokens = TextUtils.longest_common_phrase(
            tokens_1=tokens_1,
            tokens_2=tokens_2)

        if not common_tokens:
            return text_2

        common_phrase = ' '.join(common_tokens).strip().lower()
        text_2_lower = text_2.lower()

        if common_phrase not in text_2_lower:
            if self.isEnabledForWarning:
                self.logger.warning('\n'.join([
                    f"Common Phrase Not Found in Text 2",
                    f"\tCommon Phrase: {common_phrase}",
                    f"\tText 2: {text_2_lower}"]))
            return text_2_lower

        x = text_2_lower.index(common_phrase)
        y = x + len(common_phrase)

        start = text_2[:x]
        mid = f"*{text_2[x:y]}*"
        end = text_2[y:]

        final = f"{start} {mid} {end}"
        while '  ' in final:
            final = final.replace('  ', ' ').strip()

        return final
