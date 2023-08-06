from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.delete_completed_job_response_200_flow_status_modules_item_branch_chosen import (
    DeleteCompletedJobResponse200FlowStatusModulesItemBranchChosen,
)
from ..models.delete_completed_job_response_200_flow_status_modules_item_branchall import (
    DeleteCompletedJobResponse200FlowStatusModulesItemBranchall,
)
from ..models.delete_completed_job_response_200_flow_status_modules_item_iterator import (
    DeleteCompletedJobResponse200FlowStatusModulesItemIterator,
)
from ..models.delete_completed_job_response_200_flow_status_modules_item_type import (
    DeleteCompletedJobResponse200FlowStatusModulesItemType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteCompletedJobResponse200FlowStatusModulesItem")


@attr.s(auto_attribs=True)
class DeleteCompletedJobResponse200FlowStatusModulesItem:
    """ """

    type: DeleteCompletedJobResponse200FlowStatusModulesItemType
    id: Union[Unset, str] = UNSET
    job: Union[Unset, str] = UNSET
    count: Union[Unset, int] = UNSET
    iterator: Union[Unset, DeleteCompletedJobResponse200FlowStatusModulesItemIterator] = UNSET
    flow_jobs: Union[Unset, List[str]] = UNSET
    branch_chosen: Union[Unset, DeleteCompletedJobResponse200FlowStatusModulesItemBranchChosen] = UNSET
    branchall: Union[Unset, DeleteCompletedJobResponse200FlowStatusModulesItemBranchall] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id
        job = self.job
        count = self.count
        iterator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.iterator, Unset):
            iterator = self.iterator.to_dict()

        flow_jobs: Union[Unset, List[str]] = UNSET
        if not isinstance(self.flow_jobs, Unset):
            flow_jobs = self.flow_jobs

        branch_chosen: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.branch_chosen, Unset):
            branch_chosen = self.branch_chosen.to_dict()

        branchall: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.branchall, Unset):
            branchall = self.branchall.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if job is not UNSET:
            field_dict["job"] = job
        if count is not UNSET:
            field_dict["count"] = count
        if iterator is not UNSET:
            field_dict["iterator"] = iterator
        if flow_jobs is not UNSET:
            field_dict["flow_jobs"] = flow_jobs
        if branch_chosen is not UNSET:
            field_dict["branch_chosen"] = branch_chosen
        if branchall is not UNSET:
            field_dict["branchall"] = branchall

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = DeleteCompletedJobResponse200FlowStatusModulesItemType(d.pop("type"))

        id = d.pop("id", UNSET)

        job = d.pop("job", UNSET)

        count = d.pop("count", UNSET)

        iterator: Union[Unset, DeleteCompletedJobResponse200FlowStatusModulesItemIterator] = UNSET
        _iterator = d.pop("iterator", UNSET)
        if not isinstance(_iterator, Unset):
            iterator = DeleteCompletedJobResponse200FlowStatusModulesItemIterator.from_dict(_iterator)

        flow_jobs = cast(List[str], d.pop("flow_jobs", UNSET))

        branch_chosen: Union[Unset, DeleteCompletedJobResponse200FlowStatusModulesItemBranchChosen] = UNSET
        _branch_chosen = d.pop("branch_chosen", UNSET)
        if not isinstance(_branch_chosen, Unset):
            branch_chosen = DeleteCompletedJobResponse200FlowStatusModulesItemBranchChosen.from_dict(_branch_chosen)

        branchall: Union[Unset, DeleteCompletedJobResponse200FlowStatusModulesItemBranchall] = UNSET
        _branchall = d.pop("branchall", UNSET)
        if not isinstance(_branchall, Unset):
            branchall = DeleteCompletedJobResponse200FlowStatusModulesItemBranchall.from_dict(_branchall)

        delete_completed_job_response_200_flow_status_modules_item = cls(
            type=type,
            id=id,
            job=job,
            count=count,
            iterator=iterator,
            flow_jobs=flow_jobs,
            branch_chosen=branch_chosen,
            branchall=branchall,
        )

        delete_completed_job_response_200_flow_status_modules_item.additional_properties = d
        return delete_completed_job_response_200_flow_status_modules_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
