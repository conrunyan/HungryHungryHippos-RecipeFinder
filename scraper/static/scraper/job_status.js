'use strict'

$(document).ready(function() {
  refreshStatus();
  //setInterval(refreshStatus, 5000);

  function refreshStatus() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', JOB_URL, true);
    xhr.onreadystatechange = function() {
      if(xhr.readyState == 4 && xhr.status == 200) {
        updateStatus(xhr.responseText);
      }
    }
    xhr.send();
  };

  function updateStatus(e) {
    let response = JSON.parse(e);
    let container = $('#result-status-container');
    container.empty();
    container.append($('<thead><tr><th>Result</th><th>Time</th><th>Error Type</th><th>Error</th></tr></thead>'));
    container.append($('<tbody>'));

    response.results.forEach(result => {
      let domid = "result-status-" + result.id;
      // Check if element already exists
      if($("#" + domid).length == 0) {
        let element = createElement(domid, result);
        container.append(element);
      }
    });

    container.append($('</tbody>'));
  };

  function createElement(id, result) {
    let html = '<tr id=' + id + '>';

    html += htmlifySuccess(result);
    html += htmlifyDateTime(result);
    html += htmlifyErrorType(result);
    html += htmlifyError(result);

    html += '</tr>';

    return $(html);
  }

  function htmlifySuccess(result) {
    var html = '<td class="';
    if(result.successful) {
      html += "text-success";
    } else {
      html += "text-danger";
    }
    html += '">';

    if(result.successful) {
      html += "Success";
    } else {
      html += "Failure";
    }

    html += "</td>";

    return html;
  }

  function htmlifyDateTime(result) {
    var html = '<td>';
    html += formatDateTime(result.scrape_time);
    html += '</td>';
    return html;
  }

  function formatDateTime(str) {
    var date = new Date(str);
    var year = date.getFullYear();
    // Pad values to 2 digits
    var month = (date.getMonth() + 1).toString().paddingLeft("00");
    var day = date.getDate().toString().paddingLeft("00");
    var hours = date.getHours().toString().paddingLeft("00");
    var minutes = date.getMinutes().toString().paddingLeft("00");
    var seconds = date.getSeconds().toString().paddingLeft("00");
    return '{0}/{1}/{2} {3}:{4}:{5}'.format(year, month, day, hours, minutes, seconds);
  };

  function htmlifyErrorType(result) {
    var html = '<td>';
    html += result.error_type;
    html += '</td>';
    return html;
  }

  function htmlifyError(result) {
    var html = '<td>';
    var error = result.error.slice(0, 60);
    error = error.replace(/&/g, '&amp;');
    error = error.replace(/</g, '&lt;');
    error = error.replace(/>/g, '&gt;');
    html += error;
    html += '</td>';
    return html;
  }

  String.prototype.format = function() {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
      var regexp = new RegExp('\\{'+i+'\\}', 'gi');
      formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
  };

  String.prototype.paddingLeft = function (paddingValue) {
    return String(paddingValue + this).slice(-paddingValue.length);
  };
});
