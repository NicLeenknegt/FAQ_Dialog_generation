import json

class JsonReader:

    def read_attribute(self, json_obj, *attrs):
        def read_attribute_rec(json_obj, attrs):
            if len(attrs) > 0:
                attr = attrs[0]
                attrs.remove(attrs[0])
                if attr in json_obj:
                    if json_obj.get(attr) is not None:
                        return read_attribute_rec(json_obj[attr], attrs)
                    else:
                        return None
                else:
                    return None
            else:
                return json_obj
        return read_attribute_rec(json_obj, list(attrs))