function refreshJobs() {
    fetch('/api/jobs')
        .then(response => response.json())
        .then(jobs => {
            const tbody = document.querySelector('#jobs-table tbody');
            let hasPending = false;
            
            const rows = jobs.map(job => {
                if (job.status === 'pending') hasPending = true;
                
                let actionHtml = '';
                if (job.status === 'completed') {
                    actionHtml = `<a href="/preview/${job.file_path}" target="_blank" class="btn btn-sm btn-outline">Preview</a>`;
                } else if (job.status === 'failed') {
                    actionHtml = `<span class="error-text" title="${job.error_message}">Error</span>`;
                } else {
                    actionHtml = `<span class="loading-spinner"></span>`;
                }

                return `
                    <tr>
                        <td>${job.product_name || job.product_url}</td>
                        <td>${job.created_at}</td>
                        <td>
                            <span class="status-badge status-${job.status}">
                                ${job.status}
                            </span>
                        </td>
                        <td>${actionHtml}</td>
                    </tr>
                `;
            });
            
            tbody.innerHTML = rows.join('');
            
            // If there are pending jobs, refresh again in 3 seconds
            if (hasPending) {
                setTimeout(refreshJobs, 3000);
            }
        });
}

// Initial check if there are pending jobs
document.addEventListener('DOMContentLoaded', () => {
    const pendingBadges = document.querySelectorAll('.status-pending');
    if (pendingBadges.length > 0) {
        setTimeout(refreshJobs, 3000);
    }
});
