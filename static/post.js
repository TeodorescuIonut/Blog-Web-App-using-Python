
  function get_info(post_id){
//  Create Elements
      var container = document.createElement('div')
      var row = document.createElement('div')
      var col = document.createElement('div')
      var blog_post = document.createElement('div')
      var image = document.createElement('img')
      var post_title = document.createElement('h2')
      var post_date = document.createElement('p')
      var post_owner = document.createElement('a')
      var post_content = document.createElement('p')
      var owner_id

      fetch(`/api/post/${post_id}/`)
          .then(function (response) {
              return response.json();
          }).then(function (data) {
              image.src = data.image;
              post_title.innerHTML = data.title;
              post_date.innerHTML = data.creation_date;
              post_owner.innerHTML = " by " + data.owner;
              post_content.innerHTML = data.content
              owner_id = data.owner_id
              post_owner.href = `/USER/VIEW/${owner_id}`
          });
//  Add Classes
      row.classList.add("row")
      col.classList.add("col-md-12", "blog-main")
      image.classList.add("card-img-top", "view-picture")
      blog_post.classList.add("blog-post")
      post_title.classList.add("blog-post-title")
      post_date.classList.add("d-inline", "blog-post-meta")
      post_owner.classList.add("d-inline", "blog-post-meta")
      container.classList.add("container", "post")
      post_content.classList.add("post-content")
      document.body.appendChild(container)
      container.appendChild(row)
      row.appendChild(col)
      col.appendChild(blog_post)
      blog_post.appendChild(image)
      blog_post.appendChild(post_title)
      blog_post.appendChild(post_date)
      blog_post.appendChild(post_owner)
      blog_post.appendChild(post_content)
  }
