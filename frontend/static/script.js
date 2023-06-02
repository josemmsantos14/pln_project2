$(document).ready(function () {
  $("#example").DataTable();
});

function deleteTerm(designation) {
  $.ajax("/delete/" + designation, {
    type: "DELETE",
    success: function (data) {
      // window.location.href = "/terms";
      location.reload();
      fetchData();
    },
    error: function (error) {
      console.error("Error:", error);
    },
  });
}

function fetchData() {
  // Make an AJAX request to fetch the updated data
  $.ajax("/data", {
    type: "GET",
    success: function (data) {
      // Update the displayed data on the page
      // You can use this data to update your HTML elements
      console.log(data);
    },
    error: function (error) {
      console.error("Error:", error);
    },
  });
}
