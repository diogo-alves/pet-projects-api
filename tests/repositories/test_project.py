from typing import List

import pytest

from app.models import Project


@pytest.fixture
def project(project_repository, user) -> Project:
    project = Project(
        title='Project1',
        description='My project',
        url='myproject.com',
        owner_id=user.id,
    )
    return project_repository.add(project)


@pytest.fixture
def projects(project_repository, users) -> List[Project]:
    project1 = Project(
        title='Project1',
        description='My First project',
        url='myproject1.com',
        owner_id=users[0].id,
    )
    project2 = Project(
        title='Project1',
        description='My Second project',
        url='myproject2.com',
        owner_id=users[1].id,
    )
    project3 = Project(
        title='Project3',
        description='My Third project',
        url='myproject3.com',
        owner_id=users[1].id,
    )
    return [
        project_repository.add(project1),
        project_repository.add(project2),
        project_repository.add(project3),
    ]


def test_add_should_save_a_new_project_in_db(project_repository, user):
    project = Project(
        title='Project1',
        description='My project',
        url='myproject.com',
        owner_id=user.id,
    )
    saved_project = project_repository.add(project)
    assert isinstance(saved_project, Project)
    assert saved_project.id is not None


def test_list_should_retrieve_a_list_of_projects(project_repository, projects):
    result = project_repository.list(skip=0, limit=10)
    assert isinstance(result, list)
    assert all(isinstance(project, Project) for project in result)
    assert len(result) == 3


def test_list_should_skip_an_project(project_repository, projects):
    result = project_repository.list(skip=1, limit=10)
    assert len(result) == 2


def test_list_should_limit_the_retrieved_projects(
    project_repository, projects
):
    result = project_repository.list(skip=0, limit=1)
    assert len(result) == 1


def test_filter_should_retrieve_a_filtered_list_of_projects(
    project_repository, projects, users
):
    result = project_repository.filter(skip=0, limit=10, owner_id=users[1].id)
    assert isinstance(result, list)
    assert all(isinstance(project, Project) for project in result)
    assert len(result) == 2


def test_get_should_retrieve_project_if_exists(project_repository, project):
    assert project_repository.get(id=project.id) == project


def test_get_should_return_none_if_project_does_not_exist(
    project_repository, projects
):
    assert project_repository.get(id=None) is None


def test_update_should_update_project_in_db(project_repository, project):
    project.title = 'My Best Project'
    updated_project = project_repository.update(project)
    assert updated_project.id == project.id
    assert updated_project.title == 'My Best Project'


def test_remove_should_delete_project_in_db(project_repository, project):
    project_repository.remove(project)
    assert project_repository.get(id=project.id) is None
