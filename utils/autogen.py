def get_obj_fields(obj):
    fields = map(
        lambda n: '"' + (n[0:-1] if n[-1] == "_" else n) + '"',
        list(obj.__fields__.keys()),
    )

    return list(fields)


def format_fields_to_select_sql(fields: list[str]):
    return ",".join(list(fields))


def format_fields_to_update_sql(fields: list[str]):
    edit_fields = ",".join(
        list(
            map(
                lambda n: n + '=%s',
                fields,
            )
        )
    )
    return edit_fields


def merge_data(obj, old_data: dict, new_data) -> tuple:
    merged_data = list()

    fields = get_obj_fields(obj)

    for i, field_name in enumerate(fields):
        f_name = field_name.replace('"', "")
        field_value = dict(new_data)[list(obj.__fields__.keys())[i]] or old_data[f_name]
        merged_data.append(field_value)

    merged_data = tuple(merged_data)
    return merged_data
