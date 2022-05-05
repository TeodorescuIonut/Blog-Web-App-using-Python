class PostPreview:
    def __init__(self, post_id, title, contents, owner, creation_date, modification_date):
        self.id = post_id
        self.title = str(title)
        self.contents_preview = str(contents)
        self.owner = str(owner)
        self.created_at = creation_date
        self.modified_at = modification_date
