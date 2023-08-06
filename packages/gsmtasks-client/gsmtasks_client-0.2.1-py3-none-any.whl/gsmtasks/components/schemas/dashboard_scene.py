from __future__ import annotations

import typing
import lapidary_base
import pydantic
import datetime
import gsmtasks.components.schemas.account_user
import gsmtasks.components.schemas.legacy_task
import gsmtasks.components.schemas.order
import gsmtasks.components.schemas.task_metadata
import gsmtasks.components.schemas.worker_feature
import lapidary_base.absent


class DashboardSceneAssignedTaskCounts(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class DashboardScene(pydantic.BaseModel):
    orders: typing.Annotated[
        list[
            gsmtasks.components.schemas.order.Order,
        ],
        pydantic.Field(),
    ]

    tasks: typing.Annotated[
        list[
            gsmtasks.components.schemas.legacy_task.LegacyTask,
        ],
        pydantic.Field(),
    ]

    task_metadatas: typing.Annotated[
        list[
            gsmtasks.components.schemas.task_metadata.TaskMetadata,
        ],
        pydantic.Field(),
    ]

    assigned_task_counts: typing.Annotated[
        typing.Union[
            DashboardSceneAssignedTaskCounts,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    workers: typing.Annotated[
        list[
            gsmtasks.components.schemas.account_user.AccountUser,
        ],
        pydantic.Field(),
    ]

    worker_features: typing.Annotated[
        list[
            gsmtasks.components.schemas.worker_feature.WorkerFeature,
        ],
        pydantic.Field(),
    ]

    updated_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


DashboardSceneAssignedTaskCounts.update_forward_refs()
DashboardScene.update_forward_refs()
