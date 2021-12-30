import pytest

from app.exceptions import NotFoundError
from app.models import Project
from app.schemas import ProjectIn
from app.services import ProjectService


@pytest.fixture
def project_service(project_repository):
    return ProjectService(project_repository)


def test_create_project_should_return_a_project(project_service, user):
    payload = ProjectIn(
        title='First Project',
        description='My First Project',
        url='http://firstproject.com',
    )
    project_created = project_service.create(payload, owner_id=user.id)
    assert isinstance(project_created, Project)


def test_get_project_by_id_should_return_a_project(project_service, project):
    assert project_service.get_by_id(project.id) == project


def test_get_project_by_id_should_raise_an_error_if_project_does_not_exist(
    project_service, project
):
    with pytest.raises(NotFoundError):
        project_service.get_by_id(999)


def test_list_projects(project_service, projects):
    result = project_service.list(skip=0, limit=10)
    assert len(result) == 3


def test_filter_projects_by_owner(project_service, projects, users):
    result = project_service.filter_by_owner(
        skip=0, limit=10, owner_id=users[1].id
    )
    assert len(result) == 2


def test_update_project_should_return_the_project_updated(
    project_service, project
):
    payload = ProjectIn(
        title='First Project',
        description='My First Project',
        url='http://firstproject.com',
    )
    project_updated = project_service.update(project, payload)
    assert project_updated.id == project.id
    assert project_updated.title == payload.title


def test_delete_project(project_service, project):
    project_service.delete(project)
    assert project not in project_service.list(skip=0, limit=10)
