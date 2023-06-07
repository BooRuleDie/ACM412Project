import { useState, useEffect } from "react";
import axios from "axios";

export default function App() {
    const [comments, setComments] = useState([]);
    const [startIndex, setStartIndex] = useState(0);
    const [isLastFetch, setIsLastFetch] = useState(false);
    const [topicUUID, setTopicUUID] = useState(() => {
        return window.location.pathname.split("/").at(-2);
    });

    useEffect(() => {
        axios
            .get(
                `http://localhost:8000/api/comment/${topicUUID}/${startIndex}/${
                    startIndex + 4
                }/`
            )
            .then((res) => {
                if (res.data.length < 4) setIsLastFetch(true);
                setComments((prevComments) => [...prevComments, ...res.data]);
                console.log(res.data);
            })
            .catch((err) => {
                console.log(err);
            });
    }, [startIndex]);

    function handleVote(commentObj, option) {
        axios
            .get(
                `http://localhost:8000/api/vote/${option}/${commentObj.comment_id}/`
            )
            .then((res) => {
                console.log(res.data);
                if (res.data.success === 0) {
                    window.location.assign('/login/');
                } else if (res.data.success === 1) {
                    axios
                        .get(
                            `http://localhost:8000/api/comment/${topicUUID}/0/${
                                startIndex + 4
                            }/`
                        )
                        .then((response) => {
                            setComments(response.data);
                            console.log(response.data);
                        })
                        .catch((error) => {
                            console.log(error);
                        });
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }

    return (
        <>
            <div className="container border rounded-3 mb-4">
                {comments.map((comment, index) => (
                    <div
                        key={comment.comment_id}
                        className={
                            index % 2 === 0
                                ? "me-auto border rounded-3 p-4 m-5 position-relative topic-comment"
                                : "ms-auto border rounded-3 p-4 m-5 position-relative topic-comment"
                        }
                    >
                        {comment.comment_content}
                        {/* Upvote Downvote Div  */}
                        <div
                            className="d-flex position-absolute fw-bold"
                            style={{
                                bottom: "-18px",
                                cursor: "pointer",
                            }}
                        >
                            <div
                                onClick={() => handleVote(comment, "upvote")}
                                className="border border-1 rounded-5 p-1 me-2"
                                style={{
                                    backgroundColor: "rgb(231, 230, 230)",
                                }}
                            >
                                <img
                                    src="/static/up.png"
                                    alt="upvote icon"
                                    width="20px"
                                />
                                {comment.comment_upvotes}
                            </div>
                            <div
                                onClick={() => handleVote(comment, "downvote")}
                                className="border border-1 rounded-5 p-1"
                                style={{
                                    backgroundColor: "rgb(231, 230, 230)",
                                }}
                            >
                                <img
                                    src="/static/down.png"
                                    alt="downvote icon"
                                    width="20px"
                                />
                                {comment.comment_downvotes}
                            </div>
                        </div>
                        {/* Username Badge Div */}
                        <div
                            className="position-absolute"
                            style={{ top: "-14px" }}
                        >
                            <h5 className="text-center mb-4">
                                <span className="badge bg-secondary">
                                    <a
                                        href={`/profile/${comment.comment_user_id}`}
                                    >
                                        {comment.comment_username}
                                    </a>
                                </span>
                            </h5>
                        </div>
                    </div>
                ))}
            </div>

            {!isLastFetch && (
                <button
                    className="btn btn-outline-warning mx-auto my-5 d-block"
                    onClick={() => setStartIndex(startIndex + 4)}
                >
                    Load More Comments
                </button>
            )}
        </>
    );
}
