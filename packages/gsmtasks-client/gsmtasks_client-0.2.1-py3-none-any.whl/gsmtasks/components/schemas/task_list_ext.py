from __future__ import annotations

import typing
import lapidary_base
import pydantic
import gsmtasks.components.schemas.document
import gsmtasks.components.schemas.task_metadata
import gsmtasks.components.schemas.task_serializer_v2
import lapidary_base.absent


class TaskListExt(pydantic.BaseModel):
    tasks: typing.Annotated[
        list[
            gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
        ],
        pydantic.Field(),
    ]

    documents: typing.Annotated[
        typing.Union[
            list[
                gsmtasks.components.schemas.document.Document,
            ],
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    metadatas: typing.Annotated[
        typing.Union[
            list[
                gsmtasks.components.schemas.task_metadata.TaskMetadata,
            ],
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.forbid


TaskListExt.update_forward_refs()
