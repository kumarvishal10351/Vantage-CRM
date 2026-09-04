from typing import List
from sqlalchemy.orm import Session
from backend.app.repositories.opportunity_repository import OpportunityRepository
from backend.app.schemas.pipeline import (
    PipelineSummary, StageBreakdownItem, PipelineDimensionItem
)

class PipelineService:
    def __init__(self, db: Session):
        self.repo = OpportunityRepository(db)

    def get_summary(self) -> PipelineSummary:
        data = self.repo.get_pipeline_summary()
        return PipelineSummary(**data)

    def get_stages(self) -> List[StageBreakdownItem]:
        stages = self.repo.get_stage_breakdown()
        return [StageBreakdownItem(**s) for s in stages]

    def get_dimension_breakdown(self, dimension: str) -> List[PipelineDimensionItem]:
        items = self.repo.get_dimension_breakdown(dimension)
        return [PipelineDimensionItem(**i) for i in items]
