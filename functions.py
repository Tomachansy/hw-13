import json


def get_json(file):
    with open(file, "r", encoding="utf=8") as f:
        return json.load(f)


def get_tags(data):
    tag_list = set()
    for posts in data:
        contents = posts["content"]
        cont = contents.split(" ")

        for tag in cont:
            if tag.startswith("#"):
                tag_list.add(tag[1:])
    return tag_list


def get_post_by_tag(data, tag):
    posts = []
    for post in data:
        if f"#{tag}" in post["content"]:
            posts.append(post)
    return posts


def get_post(data, post, file):
    data.append(post)
    with open(file, "w", encoding="utf=8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
