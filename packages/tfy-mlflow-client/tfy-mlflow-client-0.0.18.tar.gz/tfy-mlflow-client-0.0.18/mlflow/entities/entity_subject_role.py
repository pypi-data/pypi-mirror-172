import typing

from mlflow.entities import EntityType, Role, SubjectType
from mlflow.protos.service_pb2 import SubjectRoles as ProtoEntitySubjectRoles


class EntitySubjectRole:
    def __init__(
        self,
        entity_type: str,
        entity_id: str,
        subject_type: str,
        subject_id: str,
        role: int,
        created_at: typing.Optional[int],
        updated_at: typing.Optional[int],
        tenant_name: str,
    ):
        self._entity_type = EntityType(entity_type)
        self._entity_id = entity_id
        self._subject_type = SubjectType(subject_type)
        self._subject_id = subject_id
        self._role = Role(role)
        self._created_at = created_at
        self._updated_at = updated_at
        self._tenant_name = tenant_name

    @property
    def entity_type(self) -> EntityType:
        return self._entity_type

    @property
    def entity_id(self) -> str:
        return self._entity_id

    @property
    def subject_type(self) -> SubjectType:
        return self._subject_type

    @property
    def subject_id(self) -> str:
        return self._subject_id

    @property
    def role(self) -> Role:
        return self._role

    @property
    def created_at(self) -> typing.Optional[int]:
        return self._created_at

    @property
    def updated_at(self) -> typing.Optional[int]:
        return self._updated_at

    @property
    def tenant_name(self) -> str:
        return self._tenant_name

    def to_proto(self):
        entity_subject_role = ProtoEntitySubjectRoles()
        entity_subject_role.entity_type = self.entity_type.value
        entity_subject_role.entity_id = self.entity_id
        entity_subject_role.subject_type = self.subject_type.value
        entity_subject_role.subject_id = self.subject_id
        entity_subject_role.role = self.role.name
        if self.created_at:
            entity_subject_role.created_at = self.created_at
        if self.updated_at:
            entity_subject_role.updated_at = self.updated_at
        entity_subject_role.tenant_name = self.tenant_name
        return entity_subject_role
