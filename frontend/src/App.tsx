import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ArticlesList from "./pages/ArticlesList";
import ArticleDetail from "./pages/ArticleDetail";

const App: React.FC = () => {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<ArticlesList />} />
				<Route path="/article/:id" element={<ArticleDetail />} />
        
			</Routes>
		</Router>
	);
};

export default App;
