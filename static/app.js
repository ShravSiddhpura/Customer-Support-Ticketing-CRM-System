const API_URL = '/api/tickets';
let currentTicketId = null; 

async function fetchTickets() {
    const statusFilter = document.getElementById('statusFilter').value;
    const sortFilter = document.getElementById('sortFilter').value; 
    
    let url = API_URL;
    const params = [];
    if (statusFilter) params.push(`status=${encodeURIComponent(statusFilter)}`);
    if (sortFilter) params.push(`sort_by=${encodeURIComponent(sortFilter)}`); 
    if (params.length > 0) url += '?' + params.join('&');

    try {
        const response = await fetch(url);
        const tickets = await response.json();
        
        const tableBody = document.getElementById('ticketTableBody');
        tableBody.innerHTML = ''; 

        if (tickets.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="7" class="p-8 text-center text-gray-400 font-medium">No tickets found.</td></tr>`;
            return;
        }

        tickets.forEach(ticket => {
            const date = new Date(ticket.created_at).toLocaleDateString();
            
            // Highly translucent iOS-style Status Badges
            let statusColor = 'bg-gray-400/10 text-gray-600 border-gray-400/20';
            if (ticket.status === 'Open') statusColor = 'bg-[#6a5db8]/10 text-[#6a5db8] border-[#6a5db8]/20';
            if (ticket.status === 'In Progress') statusColor = 'bg-amber-400/10 text-amber-700 border-amber-400/20';
            if (ticket.status === 'Closed') statusColor = 'bg-gray-400/10 text-gray-500 border-gray-400/20';

            // Translucent Priority Badges
            let priorityColor = 'bg-gray-400/10 text-gray-500 border-gray-400/20';
            if (ticket.priority === 'High') priorityColor = 'bg-red-400/10 text-red-600 font-semibold border-red-400/20';
            if (ticket.priority === 'Medium') priorityColor = 'bg-orange-400/10 text-orange-600 font-medium border-orange-400/20';
            if (ticket.priority === 'Low') priorityColor = 'bg-green-400/10 text-green-600 border-green-400/20';

            const row = `
                <tr class="hover:bg-white/30 transition duration-200 group">
                    <td class="p-4 pl-6 font-semibold text-[#6a5db8]">${ticket.ticket_id}</td>
                    <td class="p-4 font-medium text-gray-800">${ticket.customer_name}</td>
                    <td class="p-4 text-gray-600 truncate max-w-xs">${ticket.subject}</td>
                    <td class="p-4">
                        <span class="px-3 py-1 rounded-full text-xs font-medium uppercase tracking-wide border backdrop-blur-sm ${priorityColor}">
                            ${ticket.priority || 'Unassigned'}
                        </span>
                    </td>
                    <td class="p-4">
                        <span class="px-3 py-1 rounded-full text-xs font-medium uppercase tracking-wide border backdrop-blur-sm ${statusColor}">
                            ${ticket.status}
                        </span>
                    </td>
                    <td class="p-4 text-gray-500 text-sm whitespace-nowrap">${date}</td>
                    <td class="p-4 pr-6">
                        <button onclick="openViewModal('${ticket.ticket_id}')" class="text-[#6a5db8] font-medium hover:text-[#524694] transition opacity-80 group-hover:opacity-100">View</button>
                    </td>
                </tr>
            `;
            tableBody.insertAdjacentHTML('beforeend', row);
        });
    } catch (error) {
        console.error("Error fetching tickets:", error);
    }
}

document.addEventListener('DOMContentLoaded', fetchTickets);

/* --- CREATE TICKET LOGIC --- */
function openCreateModal() {
    document.getElementById('createForm').reset();
    document.getElementById('createModal').classList.remove('hidden');
}

function closeCreateModal() {
    document.getElementById('createModal').classList.add('hidden');
}

async function submitCreateTicket(event) {
    event.preventDefault(); 
    
    const submitBtn = document.getElementById('createSubmitBtn');
    const originalText = submitBtn.innerText;
    submitBtn.innerText = "Analyzing & Saving...";
    submitBtn.disabled = true;
    submitBtn.classList.add('opacity-75', 'cursor-not-allowed');

    const payload = {
        customer_name: document.getElementById('c_name').value,
        customer_email: document.getElementById('c_email').value,
        subject: document.getElementById('c_subject').value,
        description: document.getElementById('c_desc').value
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            closeCreateModal();
            fetchTickets(); 
        } else {
            alert("Failed to create ticket.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Network error.");
    } finally {
        submitBtn.innerText = originalText;
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
    }
}

/* --- VIEW/UPDATE TICKET LOGIC --- */
async function openViewModal(ticket_id) {
    currentTicketId = ticket_id;
    try {
        const response = await fetch(`${API_URL}/${ticket_id}`);
        const ticket = await response.json();

        document.getElementById('v_title').innerText = ticket.subject;
        document.getElementById('v_id').innerText = ticket.ticket_id;
        document.getElementById('v_name').innerText = ticket.customer_name;
        document.getElementById('v_email').innerText = ticket.customer_email;
        document.getElementById('v_date').innerText = new Date(ticket.created_at).toLocaleString();
        document.getElementById('v_desc').innerText = ticket.description;
        document.getElementById('v_status').value = ticket.status;
        document.getElementById('v_priority').value = ticket.priority || 'Unassigned';

        document.getElementById('viewModal').classList.remove('hidden');
    } catch (error) {
        console.error("Error fetching details:", error);
    }
}

function closeViewModal() {
    document.getElementById('viewModal').classList.add('hidden');
    currentTicketId = null;
}

async function updateTicket() {
    const newStatus = document.getElementById('v_status').value;
    
    try {
        const response = await fetch(`${API_URL}/${currentTicketId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (response.ok) {
            closeViewModal();
            fetchTickets(); 
        }
    } catch (error) {
        console.error("Error updating:", error);
    }
}