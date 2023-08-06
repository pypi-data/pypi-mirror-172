import functools
import inspect
import json
import sys
import typing
from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar
from typing import Union

from pydantic import Field
from pydantic import create_model

from gwproto.decoders import Decoder
from gwproto.decoders import DecoderItem
from gwproto.decoders import Decoders
from gwproto.message import Header
from gwproto.message import Message


DEFAULT_TYPE_NAME_FIELD = "type_name"


def get_pydantic_literal_type_name(
    o: Any, type_name_field: str = DEFAULT_TYPE_NAME_FIELD
) -> str:
    if hasattr(o, "__fields__"):
        if type_name_field in o.__fields__:
            if (
                typing.get_origin(o.__fields__[type_name_field].annotation)
                == typing.Literal
            ):
                return str(o.__fields__[type_name_field].default)
    return ""


def pydantic_named_types(
    module_names: str | Sequence[str],
    modules: Optional[Sequence[Any]] = None,
    type_name_field: str = DEFAULT_TYPE_NAME_FIELD,
) -> list[Any]:
    if isinstance(module_names, str):
        module_names = [module_names]
    if unimported := [
        module_name for module_name in module_names if not module_name in sys.modules
    ]:
        raise ValueError(f"ERROR. modules {unimported} have not been imported.")
    named_types = []
    type_names: dict[str, Any] = dict()
    if modules is None:
        modules = []
    for module in [sys.modules[module_name] for module_name in module_names] + list(
        modules
    ):
        module_classes = [
            entry[1] for entry in inspect.getmembers(module, inspect.isclass)
        ]
        for module_class in module_classes:
            if type_name := get_pydantic_literal_type_name(
                module_class, type_name_field=type_name_field
            ):
                if type_name in type_names:
                    raise ValueError(
                        f"ERROR {type_name_field} ({type_name}) "
                        f"for {module_class} already seen for "
                        f"class {type_names[type_name]}"
                    )
                type_names[type_name] = module_class
                named_types.append(module_class)
    return named_types


MessageDiscriminator = TypeVar("MessageDiscriminator", bound=Message[Any])


def create_message_payload_discriminator(
    model_name: str,
    module_names: str | Sequence[str] = "",
    modules: Optional[Sequence[Any]] = None,
    explicit_types: Optional[Sequence[Any]] = None,
    type_name_field: str = DEFAULT_TYPE_NAME_FIELD,
) -> Type["MessageDiscriminator"]:
    used_types = pydantic_named_types(module_names=module_names, modules=modules)
    if explicit_types is not None:
        used_types.extend(explicit_types)
    return create_model(
        model_name,
        __base__=Message,  # type: ignore
        payload=(
            Union[tuple(used_types)],
            Field(..., discriminator=type_name_field),
        ),
    )


# TODO: type of content should be better thought out (or maybe never dict?); decode needs encoding
def gridworks_message_decoder(
    content: str | bytes | dict[str, Any],
    decoders: Decoders,
    message_payload_discriminator: Optional[Type["MessageDiscriminator"]] = None,
) -> Message[Any]:
    if isinstance(content, bytes):
        content = content.decode("utf-8")
    if isinstance(content, str):
        content = json.loads(content)
    if not isinstance(content, dict):
        raise ValueError(
            f"ERROR. decoded content has type {type(content)}; dict required"
        )
    message_dict = dict(content)
    message_dict["header"] = Header.parse_obj(content.get("header", dict()))
    message: Message[Any]
    if message_dict["header"].message_type in decoders:
        message_dict["payload"] = decoders.decode(
            message_dict["header"].message_type,
            message_dict.get("payload", dict()),
        )
        message = Message(**message_dict)
    else:
        if message_payload_discriminator is None:
            raise ValueError(
                f"ERROR. No decoder present for payload type {message_dict['header'].message_type}"
            )
        else:
            message = message_payload_discriminator.parse_obj(content)
    return message


@dataclass
class OneDecoderExtractor:
    type_name_field: str = "type_alias"
    decoder_function_name: str = "dict_to_tuple"

    def get_type_name_value(self, obj: Any) -> str:
        return getattr(obj, self.type_name_field, "")

    def extract(self, obj: Any) -> Optional[DecoderItem]:
        if type_field_value := self.get_type_name_value(obj):
            if self.decoder_function_name:
                if not hasattr(obj, self.decoder_function_name):
                    raise ValueError(
                        f"ERROR. object {obj} has no attribute named {self.decoder_function_name}"
                    )
                decoder_function = getattr(obj, self.decoder_function_name)
            else:
                decoder_function = obj
            if not callable(decoder_function):
                raise ValueError(
                    f"ERROR. object {obj} attribute {self.decoder_function_name} is not Callable"
                )
            item = DecoderItem(type_field_value, decoder_function)
        else:
            item = None
        return item


@dataclass
class PydanticExtractor(OneDecoderExtractor):
    type_name_field: str = DEFAULT_TYPE_NAME_FIELD
    decoder_function_name: str = "parse_obj"

    def get_type_name_value(self, obj: Any) -> str:
        type_name = ""
        decoder_fields = getattr(obj, "__fields__", None)
        if decoder_fields:
            model_field = decoder_fields.get(self.type_name_field, None)
            if model_field:
                type_name = getattr(model_field, "default", "")
        return type_name


class DecoderExtractor:
    _extractors: list[OneDecoderExtractor]

    def __init__(self, extractors: Optional[Sequence[OneDecoderExtractor]] = None):
        if extractors is None:
            self._extractors = [
                OneDecoderExtractor(),
                PydanticExtractor(),
            ]
        else:
            self._extractors = list(extractors)

    def decoder_item_from_object(self, obj: Any) -> Optional[DecoderItem]:
        item = None
        for extractor in self._extractors:
            item = extractor.extract(obj)
            if item is not None:
                break
        return item

    def decoder_items_from_objects(self, objs: list[Any]) -> dict[str, Decoder]:
        items = dict()
        for obj in objs:
            if (item := self.decoder_item_from_object(obj)) is not None:
                items[item.type_name] = item.decoder
        return items

    def from_objects(
        self,
        objs: list[Any],
        message_payload_discriminator: Optional[Type["MessageDiscriminator"]] = None,
    ) -> Decoders:
        d = Decoders(self.decoder_items_from_objects(objs))
        d.add_decoder(
            Message.__fields__[DEFAULT_TYPE_NAME_FIELD].default,
            functools.partial(
                gridworks_message_decoder,
                decoders=d,
                message_payload_discriminator=message_payload_discriminator,
            ),
        )
        return d
