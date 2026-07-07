document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('runBtn');
    const btnSpinner = document.getElementById('btnSpinner');
    const btnText = document.getElementById('btnText');
    const ideaInput = document.getElementById('ideaInput');
    const traceLog = document.getElementById('traceLog');
    const securityAlerts = document.getElementById('securityAlerts');
    const alertsList = document.getElementById('alertsList');
    const welcomeMessage = document.getElementById('welcomeMessage');
    const resultsContent = document.getElementById('resultsContent');
    const mcpGrounding = document.getElementById('mcpGrounding');
    const researchRoadmap = document.getElementById('researchRoadmap');
    const productBrief = document.getElementById('productBrief');
    const featuresList = document.getElementById('featuresList');
    const launchPitch = document.getElementById('launchPitch');

    runBtn.addEventListener('click', async () => {
        const idea = ideaInput.value.trim();
        if (!idea) {
            alert('Please enter a project idea first!');
            return;
        }

        // Reset UI States
        btnSpinner.classList.remove('hidden');
        btnText.textContent = 'Running GravityLab...';
        runBtn.disabled = true;
        securityAlerts.style.display = 'none';
        alertsList.innerHTML = '';
        welcomeMessage.classList.remove('hidden');
        resultsContent.classList.add('hidden');
        traceLog.innerHTML = '<div class="trace-line">Payload packaged. Sending to GravityLab API...</div>';

        try {
            const response = await fetch('/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ idea }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to complete agent pipeline execution.');
            }

            const data = await response.json();

            // Display security alerts immediately if any exist
            if (data.safety_alerts && data.safety_alerts.length > 0) {
                securityAlerts.style.display = 'block';
                data.safety_alerts.forEach(alert => {
                    const li = document.createElement('li');
                    li.textContent = alert;
                    alertsList.appendChild(li);
                });
            }

            // Simulate the sequential execution trace with short delays for the demo video presentation
            let currentLine = 0;
            const printNextTrace = () => {
                if (currentLine < data.agent_trace.length) {
                    const lineText = data.agent_trace[currentLine];
                    const div = document.createElement('div');
                    div.className = 'trace-line';
                    
                    // Style alerts and completions
                    if (lineText.includes('Security Alert') || lineText.includes('PII') || lineText.includes('injection')) {
                        div.className += ' alert';
                    } else if (lineText.includes('complete') || lineText.includes('finished')) {
                        div.className += ' success';
                    }
                    
                    div.textContent = `[${new Date().toLocaleTimeString()}] ${lineText}`;
                    traceLog.appendChild(div);
                    traceLog.scrollTop = traceLog.scrollHeight;
                    currentLine++;
                    setTimeout(printNextTrace, 600); // 600ms delay per step makes the trace feel dynamic in the demo video
                } else {
                    // Once trace printing is finished, render the results
                    welcomeMessage.classList.add('hidden');
                    resultsContent.classList.remove('hidden');
                    
                    mcpGrounding.textContent = data.grounded_research;
                    researchRoadmap.textContent = data.research_roadmap;
                    productBrief.textContent = data.product_brief;
                    
                    // Render features list
                    featuresList.innerHTML = '';
                    data.features.forEach(feat => {
                        const item = document.createElement('div');
                        item.className = 'feature-item';
                        item.textContent = feat;
                        featuresList.appendChild(item);
                    });

                    launchPitch.textContent = data.launch_pitch;

                    // Restore button
                    btnSpinner.classList.add('hidden');
                    btnText.textContent = 'Run GravityLab';
                    runBtn.disabled = false;
                }
            };

            printNextTrace();

        } catch (err) {
            const div = document.createElement('div');
            div.className = 'trace-line alert';
            div.textContent = `Error: ${err.message}`;
            traceLog.appendChild(div);
            
            btnSpinner.classList.add('hidden');
            btnText.textContent = 'Run GravityLab';
            runBtn.disabled = false;
        }
    });
});
