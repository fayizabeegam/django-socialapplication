$(document).ready(function () {

    // =========== add comment ====================

    $('.add_comment').click(function (e) {
        e.preventDefault();
        var comment = $(this).closest('.comment').find('.comment_input').val();
        if (comment != '') {
            var token = $('input[name=csrfmiddlewaretoken]').val()
            var blog_id = $(this).closest('.comment').find('.blog_id').val();
            console.log(comment, token, 'iddddd', blog_id)

            $.ajax({
                method: 'POST',
                url: '/blog/add-comment/',
                data: {
                    'comment': comment,
                    'blog_id': blog_id,
                    csrfmiddlewaretoken: token
                },
                success: function (data) {
                    $('.comment_body' + blog_id).load(location.href + " .comment_body" + blog_id);
                    $('.comment_count' + blog_id).load(location.href + " .comment_count" + blog_id);
                    document.getElementById("commentForm" + blog_id).reset();
                }
            })
        }
    })

    // ===================== edit comment ====================

    // =========== get edit comment ====================

    $(document).on('click', '.edit_comment', function (e) {
        e.preventDefault();
        var comment_id = $(this).closest('.edit_comment_container').find('.comment_id').val();
        $.ajax({
            method: 'GET',
            url: '/blog/edit-comment/',
            data: {
                'comment_id': comment_id
            },
            success: function (data) {
                $('.comment_input').val(data.comment);
                $(".add_comment").addClass("d-none");
                $(".edit_comment_btn").removeClass("d-none");
            }
        })
    })

    // =========== post edit comment ===========
    $(document).on('click', '.edit_comment_btn', function (e) {
        e.preventDefault();
        var blog_id = $(this).closest('.comment').find('.blog_id').val();
        var comment = $(this).closest('.comment').find('.comment_input').val();
        if (comment != '') {
            var token = $('input[name=csrfmiddlewaretoken]').val()

            $.ajax({
                method: 'POST',
                url: '/blog/edit-comment/',
                data: {
                    'comment': comment,
                    csrfmiddlewaretoken: token
                },
                success: function (data) {
                    $('.comment_body' + blog_id).load(location.href + " .comment_body" + blog_id);
                    $(".add_comment").removeClass("d-none");
                    $(".edit_comment_btn").addClass("d-none");
                    document.getElementById("commentForm" + blog_id).reset();
                }
            })
        }
    })

    // =========== delete comment ===========
    $(document).on('click', '.delete_comment', function (e) {
        e.preventDefault();
        var comment_id = $(this).closest('.edit_comment_container').find('.comment_id').val();
        var blog_id = $(this).closest('.edit_comment_container').find('.blog_id').val();

        $.ajax({
            method: 'GET',
            url: '/blog/delete-comment/',
            data: {
                'comment_id': comment_id,
            },
            success: function (data) {
                $('.comment_body' + blog_id).load(location.href + " .comment_body" + blog_id);
                $('.comment_count' + blog_id).load(location.href + " .comment_count" + blog_id);
            }
        })
    })

    // =========== like ===========

    $(document).on('click', '.like_btn', function (e) {
        e.preventDefault();
        var is_liked = $(this).closest('.like_container').find('.is_liked').val();

        if (is_liked === 'True') {
            var token = $('input[name=csrfmiddlewaretoken]').val()
            var blog_id = $(this).closest('.like_container').find('.blog_id').val();
            $(this).replaceWith('<span class="spinner-grow" id="unlike-spinner" role="status" aria-hidden="true"></span>');

            $.ajax({
                method: 'POST',
                url: '/blog/unlike/',
                data: {
                    'is_liked': is_liked,
                    'blog_id': blog_id,
                    csrfmiddlewaretoken: token
                },
                success: function (data) {
                    $('.like_container' + blog_id).load(location.href + " .like_container" + blog_id);
                    $('.like_count' + blog_id).load(location.href + " .like_count" + blog_id);
                    $('#unlike-spinner').replaceWith('<i class="fa-solid fa-thumbs-up text-muted"></i>');
                }
            })
        }

        else {
            var token = $('input[name=csrfmiddlewaretoken]').val()
            var blog_id = $(this).closest('.like_container').find('.blog_id').val();
            $(this).replaceWith('<span class="spinner-grow" id="like-spinner" role="status" aria-hidden="true"></span>');

            $.ajax({
                method: 'POST',
                url: '/blog/like/',
                data: {
                    'is_liked': is_liked,
                    'blog_id': blog_id,
                    csrfmiddlewaretoken: token
                },
                success: function (data) {
                    $('.like_container' + blog_id).load(location.href + " .like_container" + blog_id);
                    $('.like_count' + blog_id).load(location.href + " .like_count" + blog_id);
                    $('#like-spinner').replaceWith('<i class="fa-solid fa-thumbs-up text-primary"></i>');
                }
            })
        }
    })

    // =========== follow ============

    $(document).on('click', '.follow_btn', function (e) {
        e.preventDefault();
        var follow_user_id = $(this).closest('.follow_container').find('.follow_user_id').val();
        console.log('like_text', follow_user_id)
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $(this).replaceWith('<span class="spinner-grow" id="remove-follower-spinner" role="status" aria-hidden="true"></span>');

        $.ajax({
            method: 'POST',
            url: '/user/follow/',
            data: {
                'follow_user_id': follow_user_id,
                csrfmiddlewaretoken: token
            },
            success: function (data) {
                $('#remove-follower-spinner').replaceWith('<button class="btn btn-primary unfollow_btn following{{user.id}}">Followed</button>');
                $('.refresh_following').load(location.href + ' .refresh_following');
            }
        })
    })

    // ======== remove follower ==========

    $(document).on('click', '.remove_follower_btn', function (e) {
        e.preventDefault();
        var follower_user_id = $(this).closest('.follower_container').find('.follower_user_id').val();
        console.log('like_text', follower_user_id)
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $(this).replaceWith('<span class="spinner-grow" id="remove-follower-spinner" role="status" aria-hidden="true"></span>');

        $.ajax({
            method: 'POST',
            url: '/user/remove-follower/',
            data: {
                'follower_user_id': follower_user_id,
                csrfmiddlewaretoken: token
            },
            success: function (data) {
                $('#remove-follower-spinner').replaceWith('<button class="btn btn-secondary unfollow_btn following{{user.id}}">Removed</button>');
                $('.followers_count').load(location.href + ' .followers_count');
            }
        })
    })

    // ======== unfollow ==========

    $(document).on('click', '.unfollow_btn', function (e) {
        e.preventDefault();
        var following_user_id = $(this).closest('.following_container').find('.following_user_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $(this).replaceWith('<span class="spinner-grow" id="unfollow-spinner" role="status" aria-hidden="true"></span>');

        $.ajax({
            method: 'POST',
            url: '/user/unfollow/',
            data: {
                'following_user_id': following_user_id,
                csrfmiddlewaretoken: token
            },
            success: function (data) {
                $('#unfollow-spinner').replaceWith('<button class="btn btn-secondary unfollow_btn following{{user.id}}">Removed</button>');
                $('.following_count').load(location.href + ' .following_count');
                $('.suggestion_contaner').load(location.href + ' .suggestion_contaner');
            }
        })
    })
});

//=================cards=================//

