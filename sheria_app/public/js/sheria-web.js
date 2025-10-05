// Sheria Web JavaScript
// For web pages and forms

frappe.provide('sheria.web');

// Initialize web functionality
$(document).ready(function() {
	sheria.web.init();
});

sheria.web.init = function() {
	// Initialize service booking
	if ($('.service-booking-form').length) {
		sheria.web.init_service_booking();
	}

	// Initialize contact form
	if ($('.contact-form').length) {
		sheria.web.init_contact_form();
	}

	// Initialize testimonials
	if ($('.testimonials-section').length) {
		sheria.web.init_testimonials();
	}

	// Initialize smooth scrolling
	sheria.web.init_smooth_scrolling();

	// Initialize animations
	sheria.web.init_animations();
};

sheria.web.init_service_booking = function() {
	// Initialize service booking form
	$('.service-booking-form').on('submit', function(e) {
		e.preventDefault();
		sheria.web.submit_service_booking($(this));
	});

	// Initialize service selection
	$('.service-card-web .btn').on('click', function(e) {
		e.preventDefault();
		let serviceCard = $(this).closest('.service-card-web');
		let serviceName = serviceCard.find('h3').text();
		let servicePrice = serviceCard.find('.price').text();

		sheria.web.select_service(serviceName, servicePrice);
	});

	// Initialize date picker
	if ($.fn.datepicker) {
		$('.datepicker').datepicker({
			format: 'yyyy-mm-dd',
			autoclose: true,
			todayHighlight: true
		});
	}
};

sheria.web.init_contact_form = function() {
	// Initialize contact form
	$('.contact-form form').on('submit', function(e) {
		e.preventDefault();
		sheria.web.submit_contact_form($(this));
	});
};

sheria.web.init_testimonials = function() {
	// Initialize testimonials carousel
	if ($.fn.slick) {
		$('.testimonials-carousel').slick({
			dots: true,
			infinite: true,
			speed: 300,
			slidesToShow: 1,
			adaptiveHeight: true,
			autoplay: true,
			autoplaySpeed: 5000
		});
	}
};

sheria.web.init_smooth_scrolling = function() {
	// Smooth scrolling for anchor links
	$('a[href^="#"]').on('click', function(e) {
		e.preventDefault();
		let target = $(this.getAttribute('href'));
		if (target.length) {
			$('html, body').animate({
				scrollTop: target.offset().top - 70
			}, 1000);
		}
	});
};

sheria.web.init_animations = function() {
	// Initialize scroll animations
	$(window).on('scroll', function() {
		sheria.web.check_scroll_animations();
	});

	// Trigger initial check
	sheria.web.check_scroll_animations();
};

sheria.web.check_scroll_animations = function() {
	let scrollTop = $(window).scrollTop();
	let windowHeight = $(window).height();

	$('.animate-on-scroll').each(function() {
		let elementTop = $(this).offset().top;
		if (elementTop < scrollTop + windowHeight - 100) {
			$(this).addClass('animated');
		}
	});
};

sheria.web.select_service = function(serviceName, servicePrice) {
	// Select a service and update booking form
	$('#service_name').val(serviceName);
	$('#service_price').val(servicePrice);

	// Scroll to booking form
	$('html, body').animate({
		scrollTop: $('.service-booking-form').offset().top - 100
	}, 500);

	// Show selected service
	$('.selected-service').html(`
		<div class="alert alert-info">
			<strong>Selected Service:</strong> ${serviceName} - ${servicePrice}
		</div>
	`);

	// Highlight selected service card
	$('.service-card-web').removeClass('selected');
	$(`.service-card-web:contains("${serviceName}")`).addClass('selected');
};

sheria.web.submit_service_booking = function(form) {
	// Submit service booking
	let formData = new FormData(form[0]);
	let data = Object.fromEntries(formData);

	// Show loading
	let submitBtn = form.find('button[type="submit"]');
	let originalText = submitBtn.text();
	submitBtn.prop('disabled', true).text('Submitting...');

	// Submit booking
	frappe.call({
		method: 'sheria.api.submit_service_booking',
		args: data,
		callback: function(r) {
			submitBtn.prop('disabled', false).text(originalText);

			if (r.message && r.message.success) {
				// Show success message
				sheria.web.show_success_message('Service booking submitted successfully! We will contact you soon.');

				// Reset form
				form[0].reset();
				$('.selected-service').empty();
				$('.service-card-web').removeClass('selected');
			} else {
				// Show error message
				sheria.web.show_error_message(r.message ? r.message.error : 'An error occurred. Please try again.');
			}
		},
		error: function() {
			submitBtn.prop('disabled', false).text(originalText);
			sheria.web.show_error_message('Network error. Please check your connection and try again.');
		}
	});
};

sheria.web.submit_contact_form = function(form) {
	// Submit contact form
	let formData = new FormData(form[0]);
	let data = Object.fromEntries(formData);

	// Show loading
	let submitBtn = form.find('button[type="submit"]');
	let originalText = submitBtn.text();
	submitBtn.prop('disabled', true).text('Sending...');

	// Submit contact
	frappe.call({
		method: 'sheria.api.submit_contact',
		args: data,
		callback: function(r) {
			submitBtn.prop('disabled', false).text(originalText);

			if (r.message && r.message.success) {
				// Show success message
				sheria.web.show_success_message('Thank you for contacting us! We will get back to you soon.');

				// Reset form
				form[0].reset();
			} else {
				// Show error message
				sheria.web.show_error_message(r.message ? r.message.error : 'An error occurred. Please try again.');
			}
		},
		error: function() {
			submitBtn.prop('disabled', false).text(originalText);
			sheria.web.show_error_message('Network error. Please check your connection and try again.');
		}
	});
};

sheria.web.show_success_message = function(message) {
	// Show success message
	let alertHtml = `
		<div class="alert alert-success alert-dismissible fade show" role="alert">
			<i class="fa fa-check-circle"></i> ${message}
			<button type="button" class="close" data-dismiss="alert">
				<span aria-hidden="true">&times;</span>
			</button>
		</div>
	`;

	// Add to page
	$('body').prepend(alertHtml);

	// Auto hide after 5 seconds
	setTimeout(function() {
		$('.alert-success').fadeOut();
	}, 5000);
};

sheria.web.show_error_message = function(message) {
	// Show error message
	let alertHtml = `
		<div class="alert alert-danger alert-dismissible fade show" role="alert">
			<i class="fa fa-exclamation-triangle"></i> ${message}
			<button type="button" class="close" data-dismiss="alert">
				<span aria-hidden="true">&times;</span>
			</button>
		</div>
	`;

	// Add to page
	$('body').prepend(alertHtml);

	// Auto hide after 5 seconds
	setTimeout(function() {
		$('.alert-danger').fadeOut();
	}, 5000);
};

// Utility functions
sheria.web.format_currency = function(amount, currency = 'KES') {
	return `${currency} ${parseFloat(amount).toLocaleString()}`;
};

sheria.web.validate_email = function(email) {
	let re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	return re.test(email);
};

sheria.web.validate_phone = function(phone) {
	let re = /^[\+]?[1-9][\d]{0,15}$/;
	return re.test(phone.replace(/[\s\-\(\)]/g, ''));
};

// Service booking validation
sheria.web.validate_service_booking = function(data) {
	let errors = [];

	if (!data.service_name) errors.push('Please select a service');
	if (!data.client_name) errors.push('Client name is required');
	if (!data.client_email) errors.push('Email is required');
	if (!data.client_phone) errors.push('Phone number is required');
	if (!data.preferred_date) errors.push('Preferred date is required');

	if (data.client_email && !sheria.web.validate_email(data.client_email)) {
		errors.push('Please enter a valid email address');
	}

	if (data.client_phone && !sheria.web.validate_phone(data.client_phone)) {
		errors.push('Please enter a valid phone number');
	}

	return errors;
};

// Contact form validation
sheria.web.validate_contact = function(data) {
	let errors = [];

	if (!data.name) errors.push('Name is required');
	if (!data.email) errors.push('Email is required');
	if (!data.message) errors.push('Message is required');

	if (data.email && !sheria.web.validate_email(data.email)) {
		errors.push('Please enter a valid email address');
	}

	return errors;
};