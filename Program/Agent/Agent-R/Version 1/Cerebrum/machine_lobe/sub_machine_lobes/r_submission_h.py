


class RSubmission:
    """

    """

    id = str()
    title = str()
    comment_amount = int()


    title_kwds = list()
    title_kwd_intxn = list()
    title_kwd_intxn_size = int()

    iIO_title_relevance_scores = tuple()


    aurl_url = str()
    aurl_kwds = list()
    aurl_kwd_intxn = list()
    aurl_kwd_intxn_size = list()

    iIO_aurl_relevance_scores = tuple()


    success_probability = float()


    high_engagement_datetime = str()        # Date-Time of high-level engagement.
    evaluated_for_engagement = bool()       # Boolean indicator: if the Submission was evaluated for engagement.
    highly_engaged = bool()                 # Boolean indicator: if a comment was submitted to the Submission.
    high_utterance_content = str()          # Content of high-level engagement.



    engagement_clearance = bool()
    engaged_on = bool()


    def __init__(self, fields: tuple):
        """

        :param fields:
        """

        self.id = fields[2]
        self.title = fields[1]
        self.comment_amount = fields[0]

        self.high_utterance_content = None
        self.high_engagement_datetime = None

        self.title_kwds = fields[6]
        self.title_kwd_intxn = fields[4]
        self.aurl_kwd_intxn_size = fields[5]
        self.iIO_title_relevance_scores = tuple(fields[13][0])

        self.aurl_url = fields[12]
        self.aurl_kwds = fields[11]
        self.aurl_kwd_intxn = fields[9]
        self.aurl_kwd_intxn_size = fields[10]
        self.iIO_aurl_relevance_scores = tuple(fields[13][1])


