class PostPreview:
    def __init__(self,post_id, title, contents, creation_date, modifcation_date):
        self.post_id = post_id
        self.post_title = str(title)
        self.post_contents_preview = str(contents)
        self.post_date_creation = creation_date
        self.post_date_modification = modifcation_date
