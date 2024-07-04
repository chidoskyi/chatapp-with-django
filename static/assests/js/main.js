$(document).ready(function() {
    console.log('working');

    // Function to check the length of the input and enable/disable the button
    function checkBodyLength() {
        let bodyLength = $('#body').val().length;
        let btnSub = $('.btn-sub');

        if (bodyLength >= 1) {
            btnSub.prop('disabled', false);  // Enable the button
        } else {
            btnSub.prop('disabled', true);  // Disable the button
        }
    }

    // Event listener for changes in the textarea
    $('#body').on('input', checkBodyLength);

    $(document).on('submit', '#send-form', function(e) {
        e.preventDefault();  // Prevent the default form submission

        let _body = $('#body').val();
        let _to_user = $('#to_user').val();
        let user_profile_image_url = $(this).data('user-profile-image-url');
        let current_time = $('#current-date').val();
        let delete_direct = $(this).data('delete-direct');

        $.ajax({
            type: "POST",
            url: "/send/",  // Make sure this URL points to your view
            data: {
                body: _body,
                to_user: _to_user,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                console.log("Message sent successfully");

                // Clear the input field
                $('#body').val('');

                // Build the HTML for the new message
                let _html = `
                    <div class="chat-message-right pb-2 conversation-item me">
                        <div>
                            <a href=""><img src="${user_profile_image_url}" class="rounded-circle mr-1" alt="img" width="40" height="40"></a>
                            <div class="text-muted small text-nowrap mt-2" style="font-size:10px; color: rgba(180, 180, 180, 0);">
                                <p style="font-size:10px; color: black;">${current_time}</p>
                            </div>
                        </div>
                        <div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3 cursor conversation-item-wrapper position-relative">
                            ${_body}
                            <div class="conversation-item-dropdown">
                                <button type="button" class="conversation-item-dropdown-toggle"><i class="ri-more-2-line"></i></button>
                                <ul class="conversation-item-dropdown-list">
                                    <li><a href="#"><i class="ri-share-forward-line"></i> Forward</a></li>
                                    <li><a href="#"><svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="none" viewBox="0 0 24 24" class="icon-md-heavy mr-2"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copy</a></li>
                                    <li><a href="#"><i class="ri-edit-line"></i> Edit</a></li>
                                    <li><a href="${delete_direct}"><i class="ri-delete-bin-line"></i> Delete</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                `;

                // Append the new message to the conversation
                $('.chat-message').append(_html);
            },
            error: function(response) {
                console.error("Error sending message");
                console.error(response);
            }
        });
    });
});



	document.querySelectorAll('.conversation-item-dropdown-toggle').forEach(function(item) {
		item.addEventListener('click', function(e) {
			e.preventDefault()
			if(this.parentElement.classList.contains('active')) {
				this.parentElement.classList.remove('active')
			} else {
				document.querySelectorAll('.conversation-item-dropdown').forEach(function(i) {
					i.classList.remove('active')
				})
				this.parentElement.classList.add('active')
			}
		})
	})
	
	document.addEventListener('click', function(e) {
		if(!e.target.matches('.conversation-item-dropdown, .conversation-item-dropdown *')) {
			document.querySelectorAll('.conversation-item-dropdown').forEach(function(i) {
				i.classList.remove('active')
			})
		}
	}),

    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.copy-text').forEach(function(copyLink) {
            copyLink.addEventListener('click', function(event) {
                event.preventDefault();
                const targetSelector = this.getAttribute('data-copy-target');
                const targetElement = this.closest('.conversation-item-wrapper').querySelector(targetSelector);
                const textToCopy = targetElement.textContent || targetElement.innerText;
    
                navigator.clipboard.writeText(textToCopy).then(function() {
                    console.log('Text copied to clipboard');
                }).catch(function(err) {
                    console.error('Could not copy text: ', err);
                });
            });
        });
    });



    $(document).ready(function() {
        // Handle edit button click
        $('.edit-text').on('click', function(event) {
            event.preventDefault();
            
            const messageId = $(this).data('message-id');
            const messageBody = $(this).data('message-body');
            
            
            // Debug statements
            console.log('Edit link clicked');
            console.log('Message ID:', messageId);
            console.log('Message Body:', messageBody);
            
            // Populate the edit form with the message content
            $('#edit-body').val(messageBody);
            $('#edit-message-id').val(messageId);
            
            // Hide the send form and show the edit form
            $('#send-form').addClass('d-none');
            $('#edit-form').removeClass('d-none');
            // Change the form action to edit the message
        $('#send-form').attr('action', `/edit-message/${messageId}/`);

        // Modify the HTML to include message ID and body for editing
        
            
            // Debug statement
            console.log('Edit form displayed');
        });
    
        // Handle edit form submission
        $('#edit-form').on('submit', function(event) {
            event.preventDefault();
            
            let user_profile_image_url = $(this).data('user-profile-image-url');
            let current_time = $('#current-date').val();
            let delete_direct = $(this).data('delete-direct');
            const messageId = $('#edit-message-id').val();
            const messageBody = $(this).data('message-body');
            
            if (messageId) {
                // Debug statements
                console.log('Editing message ID:', messageId);
                console.log('Message body to be sent:', $('#edit-body').val());
                
                // Perform AJAX request to edit the message
                $.ajax({
                    type: 'POST',
                    url: `/edit-message/${messageId}/`,
                    data: {
                        body: $('#edit-body').val(),
                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    success: function(response) {
                        // Debug statements
                        console.log('Response data:', response);
                        if (response.status === 'success') {

                            let _html = `
                                            <div class="chat-message-right pb-2 conversation-item me" id="message-${messageId}">
                                                <div>
                                                    <a href=""><img src="${user_profile_image_url}" class="rounded-circle mr-1" alt="img" width="40" height="40"></a>
                                                    <div class="text-muted small text-nowrap mt-2" style="font-size:10px; color: rgba(180, 180, 180, 0);">
                                                        <p style="font-size:10px; color: black;">${current_time}</p>
                                                    </div>
                                                </div>
                                                <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-2 ml-3 cursor conversation-item-wrapper position-relative" style="margin-right: 8px;">
                                                    <div class="mgs-body">${messageBody}</div>
                                                    <div class="conversation-item-dropdown">
                                                        <button type="button" class="conversation-item-dropdown-toggle"><i class="ri-more-2-line"></i></button>
                                                        <ul class="conversation-item-dropdown-list">
                                                            <li><a href="#"><i class="ri-share-forward-line"></i> Forward</a></li>
                                                            <li><a href="#" class="edit-text" data-message-id="${messageId}" data-message-body="${messageBody}"><i class="ri-edit-line"></i> Edit</a></li>
                                                            <li><a href="${delete_direct}"><i class="ri-delete-bin-line"></i> Delete</a></li>
                                                        </ul>
                                                    </div>
                                                </div>
                                            </div>
                                        `;

                                        // Replace the existing message HTML with the modified one
                                        $(`#message-${messageId}`).replaceWith(_html);

                            // Update the message content on the page
                            $(`#message-${messageId} .mgs-body`).text($('#edit-body').val());
                            // Clear the form and restore the original action
                            $('#edit-body').val('');
                            $('#edit-message-id').val('');
                            $('#edit-form').addClass('d-none');
                            $('#send-form').removeClass('d-none');
                            // Modify the HTML to include message ID and body for editing
                            

                        } else {
                            console.error('Error editing message:', response.message);
                        }
                    },
                    error: function(response) {
                        console.error('Error editing message:', response);
                    }
                });
            }
        });
    
        // Handle send form submission
        $('#send-form').on('submit', function(event) {
            // No need to preventDefault here since it's only for sending a new message
        });
    });


    // $(document).ready(function() {
    //     $('.btn').on('click', function() {
    //         $(this).siblings('.dropdown-menu').toggle();
    //     });
    
    //     // Hide the dropdown when clicking outside of it
    //     $(document).on('click', function(event) {
    //         if (!$(event.target).closest('.dropdown-container').length) {
    //             $('.dropdown-menu').hide();
    //         }
    //     });
    // });
    
    
    


    // document.addEventListener('DOMContentLoaded', function() {
    //     document.querySelectorAll('.edit-text').forEach(function(editLink) {
    //         editLink.addEventListener('click', function(event) {
    //             event.preventDefault();
    //             const messageId = this.getAttribute('data-message-id');
    //             const messageBody = this.getAttribute('data-message-body');
                
    //             // Debug statements
    //             console.log('Edit link clicked');
    //             console.log('Message ID:', messageId);
    //             console.log('Message Body:', messageBody);
    
    //             // Populate the form with the message content
    //             document.querySelector('#body').value = messageBody;
    //             document.querySelector('#message_id').value = messageId;
    
    //             // Change the form action to edit the message
    //             const sendForm = document.querySelector('#send-form');
    //             sendForm.action = `/edit-message/${messageId}/`;
    
    //             // Debug statement
    //             console.log('Form action set to:', sendForm.action);
    //         });
    //     });
    
    //     // Restore form action to send message after submitting
    //     document.querySelector('#send-form').addEventListener('submit', function(event) {
    //         event.preventDefault();
    //         const messageId = document.querySelector('#message_id').value;
    
    //         if (messageId) {
    //             // Debug statements
    //             console.log('Editing message ID:', messageId);
    //             console.log('Message body to be sent:', document.querySelector('#body').value);
    
    //             // Perform AJAX request to edit the message
    //             fetch(`/edit-message/${messageId}/`, {
    //                 method: 'POST',
    //                 headers: {
    //                     'Content-Type': 'application/x-www-form-urlencoded',
    //                     'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
    //                 },
    //                 body: new URLSearchParams({
    //                     'body': document.querySelector('#body').value
    //                 })
    //             })
    //             .then(response => response.json())
    //             .then(data => {
    //                 // Debug statements
    //                 console.log('Response data:', data);
    //                 if (data.status === 'success') {
    //                     // Update the message content on the page
    //                     document.querySelector(`#message-${messageId} .mgs-body`).innerText = document.querySelector('#body').value;
    //                     // Clear the form and restore the original action
    //                     document.querySelector('#body').value = '';
    //                     document.querySelector('#message_id').value = '';
    //                     document.querySelector('#send-form').action = '/send/';
    //                 } else {
    //                     console.error("Error editing message: ", data.message);
    //                 }
    //             })
    //             .catch(error => console.error("Error editing message: ", error));
    //         } else {
    //             // Perform the original message sending action
    //             this.submit();
    //         }
    //     });
    // });
    
    


    


document.addEventListener('DOMContentLoaded', () => {
    const statusScroll = document.querySelector('.status-scroll');
    let isDown = false;
    let startX;
    let scrollLeft;

    statusScroll.addEventListener('mousedown', (e) => {
        isDown = true;
        statusScroll.classList.add('active');
        startX = e.pageX - statusScroll.offsetLeft;
        scrollLeft = statusScroll.scrollLeft;
        statusScroll.style.cursor = 'grabbing';
    });

    statusScroll.addEventListener('mouseleave', () => {
        isDown = false;
        statusScroll.classList.remove('active');
        statusScroll.style.cursor = 'grab';
    });

    statusScroll.addEventListener('mouseup', () => {
        isDown = false;
        statusScroll.classList.remove('active');
        statusScroll.style.cursor = 'grab';
    });

    statusScroll.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - statusScroll.offsetLeft;
        const walk = (x - startX) * 1; // Scroll speed multiplier
        statusScroll.scrollLeft = scrollLeft - walk;
    });
});

$(document).ready(function(){
    var currentIndex = 0;
    var images = [];

    $('.status-more').each(function(index){
        images.push($(this).data('img-src'));
        $(this).attr('data-index', index);
    });

    $('#imageModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        currentIndex = parseInt(button.attr('data-index'));
        var imgSrc = images[currentIndex];
        var modal = $(this);
        modal.find('.modal-body #modalImage').attr('src', imgSrc);
    });

    $('#prevButton').click(function(){
        currentIndex = (currentIndex > 0) ? currentIndex - 1 : images.length - 1;
        $('#modalImage').attr('src', images[currentIndex]);
    });

    $('#nextButton').click(function(){
        currentIndex = (currentIndex < images.length - 1) ? currentIndex + 1 : 0;
        $('#modalImage').attr('src', images[currentIndex]);
    });
});