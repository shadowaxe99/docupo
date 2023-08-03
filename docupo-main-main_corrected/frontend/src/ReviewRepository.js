import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ReviewRepository = () => {
    const [repoStructure, setRepoStructure] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetchRepoStructure();
    }, []);

    const fetchRepoStructure = async () => {
        try {
            const response = await axios.get('/api/repo-structure');
            setRepoStructure(response.data);
            setIsLoading(false);
        } catch (error) {
            console.error('Error fetching repository structure:', error);
        }
    };

    const handleApprove = async () => {
        try {
            await axios.post('/api/approve-repo', { repoStructure });
            alert('Repository structure approved. Creating GitHub repository...');
        } catch (error) {
            console.error('Error approving repository structure:', error);
        }
    };

    if (isLoading) {
        return <div>Loading repository structure...</div>;
    }

    return (
        <div>
            <h1>Review Repository Structure</h1>
            <pre>{JSON.stringify(repoStructure, null, 2)}</pre>
            <button id="review-button" onClick={handleApprove}>Approve</button>
        </div>
    );
};

export default ReviewRepository;
