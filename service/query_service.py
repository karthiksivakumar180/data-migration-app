class QueryService:
    """
    Service class for handling cities.
    """

    def __init__(self, session):
        self.session = session
        # self.repository = CityRepository(session)

    def get_sample_items():
        regions = self.session.all()
        return regions
