class SocialAPI {
    static createPost(access_token, content) {
        fetch(window.location.origin + '/api/users/createPost', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                access_token: access_token,
                content: content
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                return data
            })
    }
}