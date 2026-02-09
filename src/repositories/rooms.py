from repositories import BaseRepository
from src.models.hotels import HotelsOrm


class RoomsRepository(BaseRepository):
    model = HotelsOrm