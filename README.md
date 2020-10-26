# django-query-parser
Django app to parse queries written in JSON file

## Idea
Some queries are controlled by the bussiness case, so it will be benefical if they are can changed by config file rather updating the code.

## Sample

```json
{"test":{"status_id" : 3, "name__icontains":"Ahmed"}}
```
