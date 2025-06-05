import pytest

from app.api.models import Role


class TestRoles:
    def get_roles(self, db_session):
        return db_session.query(Role).all()

    def test_check_len(self, db_session):
        roles = self.get_roles(db_session)
        assert len(roles) == 4

    def test_roles_names(self, db_session):
        roles = self.get_roles(db_session)
        role_names = [role.name for role in roles]
        assert "SuperAdmin" in role_names
        assert "Admin" in role_names
        assert "Chef" in role_names
        assert "Manager" in role_names

    def test_roles_ids(self, db_session):
        roles: list[Role] = self.get_roles(db_session)
        for role in roles:
            match role.id:
                case 1:
                    assert role.name == "SuperAdmin"
                case 2:
                    assert role.name == "Admin"
                case 3:
                    assert role.name == "Chef"
                case 4:
                    assert role.name == "Manager"
