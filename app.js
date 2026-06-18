const API_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    loadExpenses();
    loadMonthlyReports();

    document.getElementById('expense-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const date = document.getElementById('date').value;
        const category = document.getElementById('category').value;
        const amount = parseFloat(document.getElementById('amount').value);
        const description = document.getElementById('description').value;

        const expense = { date, category, amount, description };

        try {
            const response = await fetch(`${API_URL}/expenses`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(expense)
            });

            if (response.ok) {
                document.getElementById('expense-form').reset();
                loadExpenses();
                loadMonthlyReports();
            } else {
                alert('Failed to add expense');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the server');
        }
    });

    document.getElementById('export-excel').addEventListener('click', () => {
        window.location.href = `${API_URL}/export/excel`;
    });
});

async function loadExpenses() {
    try {
        const response = await fetch(`${API_URL}/expenses`);
        const expenses = await response.json();
        
        const tbody = document.getElementById('expenses-body');
        tbody.innerHTML = '';
        
        expenses.forEach(exp => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${exp.date}</td>
                <td><span style="background: #E0E7FF; color: #3730A3; padding: 4px 8px; border-radius: 999px; font-size: 0.875rem;">${exp.category}</span></td>
                <td>${exp.description}</td>
                <td style="font-weight: 600;">$${exp.amount.toFixed(2)}</td>
                <td><button class="btn-danger" onclick="deleteExpense(${exp.id})">Delete</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error loading expenses:', error);
    }
}

async function loadMonthlyReports() {
    try {
        const response = await fetch(`${API_URL}/reports/monthly`);
        const reports = await response.json();
        
        const ul = document.getElementById('monthly-list');
        ul.innerHTML = '';
        
        if (reports.length === 0) {
            ul.innerHTML = '<li style="color: #6B7280;">No data available</li>';
            return;
        }

        reports.forEach(report => {
            const li = document.createElement('li');
            
           
            const [year, month] = report.month.split('-');
            const dateObj = new Date(year, month - 1);
            const monthName = dateObj.toLocaleString('default', { month: 'short' });
            
            li.innerHTML = `
                <span class="month">${monthName} ${year}</span>
                <span class="total">$${report.total.toFixed(2)}</span>
            `;
            ul.appendChild(li);
        });
    } catch (error) {
        console.error('Error loading reports:', error);
    }
}

async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) return;
    
    try {
        const response = await fetch(`${API_URL}/expenses/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadExpenses();
            loadMonthlyReports();
        } else {
            alert('Failed to delete expense');
        }
    } catch (error) {
        console.error('Error deleting expense:', error);
    }
}
