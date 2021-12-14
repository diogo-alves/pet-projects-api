from typing import List

from fastapi import Depends

from app import models, schemas
from app.exceptions import NotFoundError
from app.repositories import ProjectRepository, Repository


class ProjectService:
    def __init__(
        self, repository: Repository = Depends(ProjectRepository)
    ) -> None:
        self.repository = repository

    def create(
        self, payload: schemas.ProjectIn, owner_id: int
    ) -> models.Project:
        fields = payload.dict()
        project = models.Project(**fields, owner_id=owner_id)
        return self.repository.add(project)

    def list(self, skip: int, limit: int) -> List[models.Project]:
        return self.repository.list(skip, limit)

    def filter_by_owner(
        self, skip: int, limit: int, owner_id: int
    ) -> List[models.Project]:
        return self.repository.filter(skip, limit, owner_id=owner_id)

    def get_by_id(self, id: int) -> models.Project:
        project = self.repository.get(id=id)
        if not project:
            raise NotFoundError()
        return project

    def update(
        self, project: models.Project, payload: schemas.ProjectIn
    ) -> models.Project:
        fields = payload.dict(exclude_unset=True)
        for field, value in fields.items():
            setattr(project, field, value)
        return self.repository.update(project)

    def delete(self, project: models.Project) -> None:
        self.repository.remove(project)
