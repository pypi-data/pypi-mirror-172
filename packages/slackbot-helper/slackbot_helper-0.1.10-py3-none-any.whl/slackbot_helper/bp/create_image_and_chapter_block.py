#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Create a Slack Block for display in Slack """


from baseblock import BaseObject


class CreateImageAndChapterBlock(BaseObject):
    """ Create a Slack Block for display in Slack 

    View Sample Output:
        https://github.com/craigtrim/climate-bot/issues/8#issue-1406861717
    """

    def __init__(self):
        """ Change Log

        Created:
            12-Oct-2022
            craigtrim@gmail.com
            *   refactored out of 'app-mention-orchestrator' in pursuit of
                https://github.com/craigtrim/climate-bot/issues/6
        Created:
            20-Oct-2022
            craigtrim@gmail.com
            *   refactored out of 'climate-bot'

        Args:
            web_client (WebClient): an instantiation of the slack client
        """
        BaseObject.__init__(self, __name__)

    def _book_name_text(self,
                        chapter: int,
                        book_name: str) -> str:
        """ Format the Provenance Description

        Args:
            chapter (int): the chapter number
            book_name (str): the name of the book (label form)

        Returns:
            str: the provenance output
            Sample Output:
                :book: How to Avoid a Climate Disaster Chapter 3:
        """

        # don't want text that says "Chapter 0"
        # the '0' chapter is always the book's Introduction
        if chapter == 0:
            return ':book: *#BOOKNAME* Introduction:'.replace(
                "#BOOKNAME", book_name)

        # Use chapter numbers as usual
        return ':book: *#BOOKNAME* Chapter #CHAPTER:'.replace(
            "#BOOKNAME", book_name).replace('#CHAPTER', str(chapter))

    @staticmethod
    def _primary_text_only(output_text: str,
                           book_name_text: str,
                           page_url: str,
                           chapter_url: str) -> list:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": output_text
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": book_name_text
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Results Page Only"
                        },
                        "url": page_url
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Entire Chapter"
                        },
                        "url": chapter_url
                    }
                ]
            }
        ]

    @staticmethod
    def _secondary_text(output_text: str,
                        output_text_secondary: list,
                        page_url: str,
                        chapter_url: str,
                        book_name_text: str) -> str:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": output_text
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": output_text_secondary
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": book_name_text
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Results Page Only"
                        },
                        "url": page_url
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Entire Chapter"
                        },
                        "url": chapter_url
                    }
                ]
            }
        ]

    def process(self,
                d_event_incoming: dict,
                output_text: str,
                output_text_secondary: list,
                page_url: str,
                chapter: int,
                chapter_url: str,
                book_name: str) -> dict:
        """ Entry Point

        Args:
            d_event_incoming (dict): the incoming event
            output_text (str): the primary output text to display to the user
            output_text_secondary (list): the secondary output text for the user
            page_url (str): the S3 Page URL
            chapter (int): the chapter number
            chapter_url (str): the S3 Chapter URL
            book_name (str): the name of the book (label form)

        Returns:
            dict: the display block
        """

        book_name_text = self._book_name_text(
            chapter=chapter,
            book_name=book_name)

        def get_thread_ts() -> str or None:
            if 'thread_ts' in d_event_incoming:
                return d_event_incoming['thread_ts']

        def decide() -> list:
            if output_text_secondary and len(output_text_secondary):
                return self._secondary_text(
                    page_url=page_url,
                    chapter_url=chapter_url,
                    book_name_text=book_name_text,
                    output_text=output_text,
                    output_text_secondary=output_text_secondary)

            return self._primary_text_only(
                page_url=page_url,
                chapter_url=chapter_url,
                output_text=output_text,
                book_name_text=book_name_text)

        blocks = decide()

        d_event_outgoing = {
            'channel': d_event_incoming['channel'],
            'blocks': blocks,
            'thread_ts': get_thread_ts(),
        }

        return d_event_outgoing
