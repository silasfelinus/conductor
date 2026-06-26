
function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }
  
  function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
  (function($) {
      'use strict';
      
      $("form.cf7sa :input").change(function() {
          var flag = 'valid';
          $('form.wpcf7-form input').each( function(i) {
              if($(this).attr('type')=='checkbox'){
                  if( $(this).closest('.wpcf7-checkbox').hasClass('wpcf7-validates-as-required') && $(this).prop('checked') != true ) {
                      flag = 'invalid';
                      jQuery('.wpcf7-submit').prop("disabled",true);
                  }
              } else if ( $(this).hasClass('wpcf7-validates-as-required') && $(this).val() == '') {
                  flag = 'invalid';
                  jQuery('.wpcf7-submit').prop("disabled",true);
              }
          });		
          if( getCookie("wp-sfrom")==1 && flag == 'valid'  ) {
              jQuery('.wpcf7-submit').prop("disabled",false);
          } else {
              jQuery('.wpcf7-submit').prop("disabled",true);
          }
      });
  
      if (typeof wpcf7 === 'undefined' || wpcf7 === null) {
          return
      }
  
      if (typeof wpcf7_cf7sa === 'undefined' || wpcf7_cf7sa === null) {
          var wpcf7_cf7sa = ''
      }
      wpcf7_cf7sa = $.extend({
          cached: 0,
          inputs: []
      }, wpcf7);
      $(function() {
          wpcf7_cf7sa.supportHtml5 = (function() {
              var features = {};
              var input = document.createElement('input');
              features.placeholder = 'placeholder' in input;
              var inputTypes = ['email', 'url', 'tel', 'number', 'range', 'date'];
              $.each(inputTypes, function(index, value) {
                  input.setAttribute('type', value);
                  features[value] = input.type !== 'text'
              });
              return features
          })();
          $('div.wpcf7 > form.cf7sa').each(function() {
              var $form = $(this);
              wpcf7_cf7sa.initForm($form);
              if (wpcf7_cf7sa.cached) {
                  wpcf7_cf7sa.refill($form)
              }
          })
      });
      wpcf7_cf7sa.getId = function(form) {
          return parseInt($('input[name="_wpcf7"]', form).val(), 10)
      };
      wpcf7_cf7sa.stripeTokenHandler = function(token, form) {
          $('input[name="stripeClientSecret"]', form).val(token)
      }
      wpcf7_cf7sa.initForm = function(form) {
          var enablePostalCode = cf7sa_object.enablePostalCode;
          if(enablePostalCode == 1){
            var enablePostalCodecf7 = true;
          }else{
            var enablePostalCodecf7 = false;
          } 
          jQuery('.wpcf7-submit').prop("disabled",true);
          var $form = $(form);
          var form_id = wpcf7_cf7sa.getId($form);
          var stripe;
          var elements;
          var cardElement;
          var paymentForm;
          if (cf7sa_object.cf7sa_stripe.hasOwnProperty(form_id)) {
              stripe = Stripe(cf7sa_object.cf7sa_stripe[form_id]);
              elements = stripe.elements();
              cardElement = elements.create('card', {
                  style: JSON.parse(cf7sa_object.cf7sa_stripe_style[form_id]),
                  hidePostalCode: enablePostalCodecf7,
              });
              cardElement.mount('#card-element-' + form_id);
              cardElement.addEventListener('change', function(event) {
                  setCookie("wp-sfrom", 0, 1);
                  jQuery('.wpcf7-submit').prop("disabled",true);
                  var displayError = document.getElementById('card-errors-' + form_id);
                  if (event.error) {
                      jQuery('.wpcf7-submit').prop("disabled",true);
                      displayError.textContent = event.error.message;					
                  } else {
                      displayError.textContent = '';
                  }
                  
                  if (event.complete) {
                      setCookie("wp-sfrom", 1, 1);
                      var flag = 'valid';
                      $('form.wpcf7-form input').each( function(i) {
                          if( $(this).hasClass('wpcf7-validates-as-required') && $(this).val() == '') {
                              flag = 'invalid';
                              jQuery('.wpcf7-submit').prop("disabled",true);
                          }
                      });
                      if( flag == 'invalid' ) {
                          jQuery('.wpcf7-submit').prop("disabled",true);
                      } else {
                          jQuery('.wpcf7-submit').prop("disabled",false);
                      } 
                  }
              })
          }
          
          $form.submit(function(event) {
              
              if( getCookie("wp-sfrom")!=1 ) {
                  return false;
              }
              
              $('.ajax-loader', $form).addClass('is-active');
              document.addEventListener('wpcf7invalid', function(event) {
                  return !1
              }, !1);
              if (!wpcf7_cf7sa.supportHtml5.placeholder) {
                  $('[placeholder].placeheld', $form).each(function(i, n) {
                      $(n).val('').removeClass('placeheld')
                  })
              }
              document.addEventListener('submit', async (e) => {
                  if( getCookie("wp-sfrom")!=1 ) {
                      return false;
                  }
                  e.preventDefault();
                  var formData = new FormData($form.get(0));
                  // Security: Add nonce for CSRF protection
                  formData.append('_wpcf7_nonce', cf7sa_object.nonce);
                  var $message = $('.wpcf7-response-output', $form);
                  var form_id = wpcf7_cf7sa.getId($form);
                  var intentresponse = "";
                  $.ajax({
                      type: 'POST',
                      url: cf7sa_object.ajax_url,
                      data: formData,
                      processData: !1,
                      contentType: !1,
                      beforeSend: function() {
                          $(".wpcf7-spinner").css("visibility", "visible");
                          $('.ajax-loader', $form).addClass('is-active');
                          $('.wpcf7-form').addClass('payment-submitting');
                          jQuery('.wpcf7-submit').prop("disabled",true);
                          var flag = 0;
                          $('form.wpcf7-form input').each( function(i) {
                              if( $(this).hasClass('wpcf7-validates-as-required') && $(this).val() == '') {
                                  $('.wpcf7-spinner').hide();
                                  $('.wpcf7-response-output').show();
                                  flag = 1;
                              }
                          });
                          if( flag == 0 ) {
                              $('.wpcf7-spinner').show();
                              $('.wpcf7-response-output').hide();
                          }
                      },
                      success: function(response) {
                          if (response!='0') {
                              jQuery('.wpcf7-submit').prop("disabled",true);
                              setCookie("wp-sfrom", 0, 1);
                              const IntentsResponse = stripe.confirmCardPayment(response, {
                                  payment_method: {
                                      card: cardElement,
                                  },
                              })
                              IntentsResponse.then(function(result) {
                                if (result.paymentIntent) {
                                    if (typeof(result.paymentIntent) !== 'undefined') {
                                        if (result.paymentIntent.status == "succeeded") {
                                            $('input[name="stripeClientSecret"]').val(result.paymentIntent.id);
                                            wpcf7_cf7sa.submit($form, result, elements, cardElement)
                                        }
                                    } else {
                                        $('.wpcf7-form').removeClass('payment-submitting');
                                        $message.html('').append('<span>'+ frontend_msg_object.undefined +'</span>').slideDown('fast');
                                        $("#please-wait").hide();
                                        $(".wpcf7-spinner").css("visibility", "hidden");
                                    }
                                } else {
                                     $('.wpcf7-form').removeClass('payment-submitting');
                                     $message.html('').append('<span>Payment is faild</span>').slideDown('fast');
                                     $("#please-wait").hide();
                                     $(".wpcf7-spinner").css("visibility", "hidden");
                                }
                            })
                          }else {
                              $('.wpcf7-form').removeClass('payment-submitting');
                              $message.html('').append('<span>Payment is faild</span>').slideDown('fast');
                              $("#please-wait").hide();
                              $(".wpcf7-spinner").css("visibility", "hidden");
                          }
                          jQuery('.wpcf7-submit').prop("disabled",false);
                      }
                  });
                  event.preventDefault()
              })
          });
  
  
          if ($($form).find('.ajax-loader').length < 1) {
              $('.wpcf7-submit', $form).after('<span class="ajax-loader"></span>')
          }
          //wpcf7_cf7sa.toggleSubmit($form);
          // $form.on('click', '.wpcf7-acceptance', function() {
          //     wpcf7_cf7sa.toggleSubmit($form)
          // });
          $('.wpcf7-exclusive-checkbox', $form).on('click', 'input:checkbox', function() {
              var name = $(this).attr('name');
              $form.find('input:checkbox[name="' + name + '"]').not(this).prop('checked', !1)
          });
          $('.wpcf7-list-item.has-free-text', $form).each(function() {
              var $freetext = $(':input.wpcf7-free-text', this);
              var $wrap = $(this).closest('.wpcf7-form-control');
              if ($(':checkbox, :radio', this).is(':checked')) {
                  $freetext.prop('disabled', !1)
              } else {
                  $freetext.prop('disabled', !0)
              }
              $wrap.on('change', ':checkbox, :radio', function() {
                  var $cb = $('.has-free-text', $wrap).find(':checkbox, :radio');
                  if ($cb.is(':checked')) {
                      $freetext.prop('disabled', !1).focus()
                  } else {
                      $freetext.prop('disabled', !0)
                  }
              })
          });
          if (!wpcf7_cf7sa.supportHtml5.placeholder) {
              $('[placeholder]', $form).each(function() {
                  $(this).val($(this).attr('placeholder'));
                  $(this).addClass('placeheld');
                  $(this).focus(function() {
                      if ($(this).hasClass('placeheld')) {
                          $(this).val('').removeClass('placeheld')
                      }
                  });
                  $(this).blur(function() {
                      if ('' === $(this).val()) {
                          $(this).val($(this).attr('placeholder'));
                          $(this).addClass('placeheld')
                      }
                  })
              })
          }
          if (wpcf7_cf7sa.jqueryUi && !wpcf7_cf7sa.supportHtml5.date) {
              $form.find('input.wpcf7-date[type="date"]').each(function() {
                  $(this).datepicker({
                      dateFormat: 'yy-mm-dd',
                      minDate: new Date($(this).attr('min')),
                      maxDate: new Date($(this).attr('max'))
                  })
              })
          }
          if (wpcf7_cf7sa.jqueryUi && !wpcf7_cf7sa.supportHtml5.number) {
              $form.find('input.wpcf7-number[type="number"]').each(function() {
                  $(this).spinner({
                      min: $(this).attr('min'),
                      max: $(this).attr('max'),
                      step: $(this).attr('step')
                  })
              })
          }
          $('.wpcf7-character-count', $form).each(function() {
              var $count = $(this);
              var name = $count.attr('data-target-name');
              var down = $count.hasClass('down');
              var starting = parseInt($count.attr('data-starting-value'), 10);
              var maximum = parseInt($count.attr('data-maximum-value'), 10);
              var minimum = parseInt($count.attr('data-minimum-value'), 10);
              var updateCount = function(target) {
                  var $target = $(target);
                  var length = $target.val().length;
                  var count = down ? starting - length : length;
                  $count.attr('data-current-value', count);
                  $count.text(count);
                  if (maximum && maximum < length) {
                      $count.addClass('too-long')
                  } else {
                      $count.removeClass('too-long')
                  }
                  if (minimum && length < minimum) {
                      $count.addClass('too-short')
                  } else {
                      $count.removeClass('too-short')
                  }
              };
              $(':input[name="' + name + '"]', $form).each(function() {
                  updateCount(this);
                  $(this).keyup(function() {
                      updateCount(this)
                  })
              })
          });
          $form.on('change', '.wpcf7-validates-as-url', function() {
              var val = $.trim($(this).val());
              if (val && !val.match(/^[a-z][a-z0-9.+-]*:/i) && -1 !== val.indexOf('.')) {
                  val = val.replace(/^\/+/, '');
                  val = 'http://' + val
              }
              $(this).val(val)
          })
      };
      wpcf7_cf7sa.submit = function(form, stripe, elements, card) {
          if (typeof window.FormData !== 'function') {
              return
          }
          var $form = $(form);
          $('.ajax-loader', $form).addClass('is-active');
          wpcf7_cf7sa.clearResponse($form);
          var formData = new FormData($form.get(0));
          var detail = {
              id: $form.closest('div.wpcf7').attr('id'),
              status: 'init',
              inputs: [],
              formData: formData
          };
          $.each($form.serializeArray(), function(i, field) {
              if ('_wpcf7' == field.name) {
                  detail.contactFormId = field.value
              } else if ('_wpcf7_version' == field.name) {
                  detail.pluginVersion = field.value
              } else if ('_wpcf7_locale' == field.name) {
                  detail.contactFormLocale = field.value
              } else if ('_wpcf7_unit_tag' == field.name) {
                  detail.unitTag = field.value
              } else if ('_wpcf7_container_post' == field.name) {
                  detail.containerPostId = field.value
              } else if (field.name.match(/^_wpcf7_\w+_free_text_/)) {
                  var owner = field.name.replace(/^_wpcf7_\w+_free_text_/, '');
                  detail.inputs.push({
                      name: owner + '-free-text',
                      value: field.value
                  })
              } else if (field.name.match(/^_/)) {} else {
                  detail.inputs.push(field)
              }
          });
          wpcf7_cf7sa.triggerEvent($form.closest('div.wpcf7'), 'beforesubmit', detail);
          var ajaxSuccess = function(data, status, xhr, $form) {
              detail.id = $(data.into).attr('id');
              detail.status = data.status;
              detail.apiResponse = data;
              var $message = $('.wpcf7-response-output', $form);
              switch (data.status) {
                  case 'validation_failed':
                      $.each(data.invalidFields, function(i, n) {
                          $(n.into, $form).each(function() {
                              wpcf7_cf7sa.notValidTip(this, n.message);
                              $('.wpcf7-form-control', this).addClass('wpcf7-not-valid');
                              $('[aria-invalid]', this).attr('aria-invalid', 'true')
                          })
                      });
                      $message.addClass('wpcf7-validation-errors');
                      $form.addClass('invalid');
                      wpcf7_cf7sa.triggerEvent(data.into, 'invalid', detail);
                      break;
                  case 'acceptance_missing':
                      $message.addClass('wpcf7-acceptance-missing');
                      $form.addClass('unaccepted');
                      wpcf7_cf7sa.triggerEvent(data.into, 'unaccepted', detail);
                      break;
                  case 'spam':
                      $message.addClass('wpcf7-spam-blocked');
                      $form.addClass('spam');
                      wpcf7_cf7sa.triggerEvent(data.into, 'spam', detail);
                      break;
                  case 'aborted':
                      $message.addClass('wpcf7-aborted');
                      $form.addClass('aborted');
                      wpcf7_cf7sa.triggerEvent(data.into, 'aborted', detail);
                      break;
                  case 'mail_sent':
                      $message.addClass('wpcf7-mail-sent-ok');
                      $form.addClass('sent');
                      wpcf7_cf7sa.triggerEvent(data.into, 'mailsent', detail);
                      break;
                  case 'mail_failed':
                      $message.addClass('wpcf7-mail-sent-ng');
                      $form.addClass('failed');
                      wpcf7_cf7sa.triggerEvent(data.into, 'mailfailed', detail);
                      break;
                  default:
                      var customStatusClass = 'custom-' + data.status.replace(/[^0-9a-z]+/i, '-');
                      $message.addClass('wpcf7-' + customStatusClass);
                      $form.addClass(customStatusClass)
              }
              wpcf7_cf7sa.refill($form, data);
              wpcf7_cf7sa.triggerEvent(data.into, 'submit', detail);
              if ( $form.hasClass('sent') ) {
                  $form.each(function() {
                      this.reset()
                  });
                  //wpcf7_cf7sa.toggleSubmit($form)
              }
              if (!wpcf7_cf7sa.supportHtml5.placeholder) {
                  $form.find('[placeholder].placeheld').each(function(i, n) {
                      $(n).val($(n).attr('placeholder'))
                  })
              }
              $message.html('').append(data.message).slideDown('fast');
              $message.attr('role', 'alert');
              $('.screen-reader-response', $form.closest('.wpcf7')).each(function() {
                  var $response = $(this);
                  $response.html('').attr('role', '').append(data.message);
                  if (data.invalidFields) {
                      var $invalids = $('<ul></ul>');
                      $.each(data.invalidFields, function(i, n) {
                          if (n.idref) {
                              var $li = $('<li></li>').append($('<a></a>').attr('href', '#' + n.idref).append(n.message))
                          } else {
                              var $li = $('<li></li>').append(n.message)
                          }
                          $invalids.append($li)
                      });
                      $response.append($invalids)
                  }
                  $response.attr('role', 'alert').focus()
              })
          };
          $.ajax({
              type: 'POST',
              url: wpcf7_cf7sa.api.getRoute('/contact-forms/' + wpcf7_cf7sa.getId($form) + '/feedback'),
              data: formData,
              dataType: 'json',
              processData: !1,
              contentType: !1
          }).done(function(data, status, xhr) {
              ajaxSuccess(data, status, xhr, $form);
              $('.ajax-loader', $form).removeClass('is-active');
              $("#please-wait").hide();
              $(".wpcf7-spinner").css("visibility", "hidden");
              $('.wpcf7-form').removeClass('payment-submitting')
          }).fail(function(xhr, status, error) {
              var $e = $('<div class="ajax-error"></div>').text(error.message);
              $form.after($e)
          })
      };
      wpcf7_cf7sa.triggerEvent = function(target, name, detail) {
          var $target = $(target);
          var event = new CustomEvent('wpcf7' + name, {
              bubbles: !0,
              detail: detail
          });
          $target.get(0).dispatchEvent(event);
          $target.trigger('wpcf7:' + name, detail);
          $target.trigger(name + '.wpcf7', detail)
      };
      /*wpcf7_cf7sa.toggleSubmit = function(form, state) {
          var $form = $(form);
          var $submit = $('input:submit', $form);
          if (typeof state !== 'undefined') {
              $submit.prop('disabled', !state);
              return
          }
          if ($form.hasClass('wpcf7-acceptance-as-validation')) {
              return
          }
          $submit.prop('disabled', !1);
          $('.wpcf7-acceptance', $form).each(function() {
              var $span = $(this);
              var $input = $('input:checkbox', $span);
              if (!$span.hasClass('optional')) {
                  if ($span.hasClass('invert') && $input.is(':checked') || !$span.hasClass('invert') && !$input.is(':checked')) {
                      $submit.prop('disabled', !0);
                      return !1
                  }
              }
          })
      };*/
      wpcf7_cf7sa.notValidTip = function(target, message) {
          var $target = $(target);
          $('.wpcf7-not-valid-tip', $target).remove();
          $('<span role="alert" class="wpcf7-not-valid-tip"></span>').text(message).appendTo($target);
          if ($target.is('.use-floating-validation-tip *')) {
              var fadeOut = function(target) {
                  $(target).not(':hidden').animate({
                      opacity: 0
                  }, 'fast', function() {
                      $(this).css({
                          'z-index': -100
                      })
                  })
              };
              $target.on('mouseover', '.wpcf7-not-valid-tip', function() {
                  fadeOut(this)
              });
              $target.on('focus', ':input', function() {
                  fadeOut($('.wpcf7-not-valid-tip', $target))
              })
          }
      };
      wpcf7_cf7sa.refill = function(form, data) {
          var $form = $(form);
          var refillCaptcha = function($form, items) {
              $.each(items, function(i, n) {
                  $form.find(':input[name="' + i + '"]').val('');
                  $form.find('img.wpcf7-captcha-' + i).attr('src', n);
                  var match = /([0-9]+)\.(png|gif|jpeg)$/.exec(n);
                  $form.find('input:hidden[name="_wpcf7_captcha_challenge_' + i + '"]').attr('value', match[1])
              })
          };
          var refillQuiz = function($form, items) {
              $.each(items, function(i, n) {
                  $form.find(':input[name="' + i + '"]').val('');
                  $form.find(':input[name="' + i + '"]').siblings('span.wpcf7-quiz-label').text(n[0]);
                  $form.find('input:hidden[name="_wpcf7_quiz_answer_' + i + '"]').attr('value', n[1])
              })
          };
          if (typeof data === 'undefined') {
              $.ajax({
                  type: 'GET',
                  url: wpcf7_cf7sa.api.getRoute('/contact-forms/' + wpcf7_cf7sa.getId($form) + '/refill'),
                  beforeSend: function(xhr) {
                      var nonce = $form.find(':input[name="_wpnonce"]').val();
                      if (nonce) {
                          xhr.setRequestHeader('X-WP-Nonce', nonce)
                      }
                  },
                  dataType: 'json'
              }).done(function(data, status, xhr) {
                  if (data.captcha) {
                      refillCaptcha($form, data.captcha)
                  }
                  if (data.quiz) {
                      refillQuiz($form, data.quiz)
                  }
              })
          } else {
              if (data.captcha) {
                  refillCaptcha($form, data.captcha)
              }
              if (data.quiz) {
                  refillQuiz($form, data.quiz)
              }
          }
      };
      wpcf7_cf7sa.clearResponse = function(form) {
          var $form = $(form);
          $form.removeClass('invalid spam sent failed');
          $form.siblings('.screen-reader-response').html('').attr('role', '');
          $('.wpcf7-not-valid-tip', $form).remove();
          $('[aria-invalid]', $form).attr('aria-invalid', 'false');
          $('.wpcf7-form-control', $form).removeClass('wpcf7-not-valid');
          $('.wpcf7-response-output', $form).hide().empty().removeAttr('role').removeClass('wpcf7-mail-sent-ok wpcf7-mail-sent-ng wpcf7-validation-errors wpcf7-spam-blocked')
      };
      wpcf7_cf7sa.api.getRoute = function(path) {
          var url = wpcf7_cf7sa.api.root + wpcf7_cf7sa.api.namespace + path;
          return url
      }
  })(jQuery);
  (function() {
      if (typeof window.CustomEvent === "function") return !1;
  
      function CustomEvent(event, params) {
          params = params || {
              bubbles: !1,
              cancelable: !1,
              detail: undefined
          };
          var evt = document.createEvent('CustomEvent');
          evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail);
          return evt
      }
      CustomEvent.prototype = window.Event.prototype;
      window.CustomEvent = CustomEvent
  })()
