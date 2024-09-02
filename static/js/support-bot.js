function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

function removeStaff(url, staff_id, ticket_id){
    showInfo("Removing "+staff_id+" staff", "Executing call");
    return $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {user_id: staff_id, ticket_id: ticket_id},
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        },
        success: (data) => {
            showSuccess("Staff removed successfully", "Success")
            console.log(data);
        },
        error: (error) => {
            showDanger(error.responseText, error.status);
            console.log(error);
        }
      });
}

function addStaff(url, staff_id, ticket_id){
    return $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {user_id: staff_id, ticket_id: ticket_id},
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        },
        success: (data) => {
          showSuccess("Staff added successfully", "Success")
          console.log(data);
        },
        error: (error) => {
          showDanger(error.responseText, error.status);
          console.log(error);
        }
      });
}

function removeChatStaff(url, staff_id, chat_room_id){
  showInfo("Removing "+staff_id+" staff", "Executing call");
  return $.ajax({
      url: url,
      type: "POST",
      dataType: "json",
      data: {user_id: staff_id, chat_room_id: chat_room_id},
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
      },
      success: (data) => {
          showSuccess("Staff removed successfully", "Success")
          console.log(data);
      },
      error: (error) => {
          showDanger(error.responseText, error.status);
          console.log(error);
      }
    });
}

function addChatStaff(url, staff_id, chat_room_id) {
  return $.ajax({
      url: url,
      type: "POST",
      dataType: "json",
      data: {user_id: staff_id, chat_room_id: chat_room_id},
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
      },
      success: (data) => {
        showSuccess("Staff added successfully", "Success")
        console.log(data);
      },
      error: (error) => {
        showDanger(error.responseText, error.status);
        console.log(error);
      }
    });
}

function reopen(url, ticket_id){
    return $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {ticket_id: ticket_id},
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        },
        success: (data) => {
          showSuccess("Ticket reopened successfully", "Success");
          console.log(data);
        },
        error: (error) => {
          showDanger(error.responseText, error.status);
          console.log(error);
        }
      });
}

function removeTicketRoom(url, ticket_id){
  return $.ajax({
      url: url,
      type: "POST",
      dataType: "json",
      data: {ticket_id: ticket_id},
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
      },
      success: (data) => {
        showSuccess("Ticket room deleted successfully", "Success");
        console.log(data);
      },
      error: (error) => {
        showDanger(error.responseText, error.status);
        console.log(error);
      }
    });
}

function removeChatRoom(url, chat_room_id){
  return $.ajax({
      url: url,
      type: "POST",
      dataType: "json",
      data: {chat_room_id: chat_room_id},
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
      },
      success: (data) => {
        showSuccess("Chat room deleted successfully", "Success");
        console.log(data);
      },
      error: (error) => {
        showDanger(error.responseText, error.status);
        console.log(error);
      }
    });
}

function close(url, ticket_id){
    return $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {ticket_id: ticket_id},
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        },
        success: (data) => {
          showSuccess("Ticket closed successfully", "Success")
          console.log(data);
        },
        error: (error) => {
          showDanger(error.responseText, error.status);
          console.log(error);
        }
      });    
}

function closeChat(url, chat_room_id){
  return $.ajax({
      url: url,
      type: "POST",
      dataType: "json",
      data: {chat_room_id: chat_room_id},
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
      },
      success: (data) => {
        showSuccess("Chat closed successfully", "Success")
        console.log(data);
      },
      error: (error) => {
        showDanger(error.responseText, error.status);
        console.log(error);
      }
    });    
}