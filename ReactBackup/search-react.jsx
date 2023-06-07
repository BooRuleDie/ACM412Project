import { useState, useEffect } from "react";
import axios from "axios";

export default function App() {
    const [searchTerm, setSearchTerm] = useState("");
    const [topics, setTopics] = useState([]);

    useEffect(() => {
        if (searchTerm !== "") {
            axios
                .get(`http://localhost:8000/api/search/${searchTerm}/`)
                .then((res) => {
                    setTopics(res.data);
                    console.log(res.data);
                })
                .catch((err) => {
                    console.log(err);
                });
        } else {
            setTopics([]);
        }
    }, [searchTerm]);

    return (
        <>
            <input
                className="form-control me-2 border-warning"
                type="search"
                placeholder="Search Topic"
                aria-label="Search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            {searchTerm && (
                <>
                    <div
                        className="position-absolute text-center border border-warning z-3"
                        id="search-results"
                        style={{backgroundColor: "#f3f3f3"}}
                    >
                        {topics.length === 0 && searchTerm !== "" && (
                            <p className=" p-2 fst-italic fw-light">No Topic :(</p>
                        )}
                        {topics.map((topic) => {
                            return (
                                <div
                                    key={topic.id}
                                    className="m-2 fw-bold p-2 rounded"
                                    style={{ backgroundColor: "#e0e0e0" }}
                                >
                                    {topic.title.slice(0, 23) + "..."}
                                </div>
                            );
                        })}
                    </div>
                </>
            )}
        </>
    );
}
