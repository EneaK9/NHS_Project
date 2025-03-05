import React, { useEffect, useState } from "react";
import { getArticles } from "../api";
import { Link } from "react-router-dom";

interface Article {
	id: number;
	translated_title: string;
	url: string;
}

const ArticlesList: React.FC = () => {
	const [articles, setArticles] = useState<Article[]>([]);

	useEffect(() => {
		const fetchArticles = async () => {
			const data = await getArticles();
			setArticles(data);
		};
		fetchArticles();
	}, []);

	return (
		<div>
			<h1>Albanian NHS Articles</h1>
			<ul>
				{articles.map((article) => (
					<li key={article.id}>
						<Link to={`/article/${article.id}`}>
							{article.translated_title}
						</Link>
                        <div>hello</div>
					</li>
				))}
			</ul>
		</div>
	);
};

export default ArticlesList;
