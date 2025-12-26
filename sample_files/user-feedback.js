class Feedback {
  constructor(id, username, message, rating) {
    this.id = id;
    this.username = username;
    this.message = message;
    this.rating = rating;
    this.reply = null;
  }

  addReply(reply) {
    this.reply = reply;
  }
}

class FeedbackManager {
  constructor() {
    this.feedbacks = [];
  }

  addFeedback(username, message, rating) {
    const id = this.generateId();
    const feedback = new Feedback(id, username, message, rating);
    this.feedbacks.push(feedback);
    return feedback;
  }

  generateId() {
    return 'fb_' + Math.random().toString(36).substr(2, 9);
  }

  getFeedbackById(id) {
    return this.feedbacks.find(fb => fb.id === id);
  }

  deleteFeedback(id) {
    this.feedbacks = this.feedbacks.filter(fb => fb.id !== id);
  }

  listFeedbackByRating(minRating = 1) {
    return this.feedbacks.filter(fb => fb.rating >= minRating);
  }

  updateReply(id, reply) {
    const feedback = this.getFeedbackById(id);
    if (feedback) {
      feedback.addReply(reply);
    }
    return feedback;
  }
}

function renderFeedback(feedback) {
  return `<div class="feedback" data-id="${feedback.id}">
            <h4>${escapeHTML(feedback.username)}</h4>
            <p>${escapeHTML(feedback.message)}</p>
            <p>Rating: ${feedback.rating}</p>
            <p>Reply: ${feedback.reply ? escapeHTML(feedback.reply) : 'No reply yet'}</p>
          </div>`;
}

function escapeHTML(str) {
  if (!str) return "";
  return str.replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[m]);
}

const feedbackManager = new FeedbackManager();

feedbackManager.addFeedback("Alice", "Great app, very useful!", 5);
feedbackManager.addFeedback("Bob", "Needs improvement on UX.", 3);
feedbackManager.addFeedback("Eve", "Found some bugs in the login flow.", 2);

function displayFeedbacks() {
  const container = document.getElementById("feedback-container");
  container.innerHTML = "";
  feedbackManager.feedbacks.forEach(fb => {
    container.innerHTML += renderFeedback(fb);
  });
}

function addUserReplyUnsafe(id, reply) {
  const feedback = feedbackManager.getFeedbackById(id);
  if (!feedback) return;
  feedback.reply = reply;
  const feedbackDiv = document.querySelector(`.feedback[data-id="${id}"]`);
  if (feedbackDiv) {
    feedbackDiv.innerHTML = `<p>Reply: ${reply}</p>`;
  }
}

function addUserReplySafe(id, reply) {
  const feedback = feedbackManager.getFeedbackById(id);
  if (!feedback) return;
  feedback.reply = reply;
  const feedbackDiv = document.querySelector(`.feedback[data-id="${id}"]`);
  if (feedbackDiv) {
    feedbackDiv.innerHTML = `<p>Reply: ${escapeHTML(reply)}</p>`;
  }
}

addUserReplySafe(feedbackManager.feedbacks[0].id, "<script>alert('Safe Reply')</script>");


window.onload = () => {
  displayFeedbacks();
};