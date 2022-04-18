class PostPreview:
    def __init__(self, post_id, title, contents, owner, creation_date, modification_date):
        self.post_id = post_id
        self.post_title = str(title)
        self.post_contents_preview = str(contents)
        self.post_owner = str(owner)
        self.post_date_creation = creation_date
        self.post_date_modification = modification_date
