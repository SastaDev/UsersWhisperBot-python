# start text
start_text = [
    '''
<b>Hello and Thanks for starting me!</b>

<b>Usage:</b>
• <b>@UsersWhisperBot</b> <i>target user</i> <u>options</u> <code>whisper text.</code>

use [] square brackets when specifying more than one target user.
<b>e.g:</b> [target user 1, target user 2, and so on...]

<b>Example:</b>
<code>@UsersWhisperBot {} This is an example.</code>
    '''
    ]

inline_usage_button_text = [
    'INLINE USAGE'
    ]

switch_inline_query_button_text = [
    'GO INLINE'
    ]

inline_usage_text = [
    '''
<b>[•] Inline Usage:</b>

• Making an inline whisper:
<b>-></b> <b>@UsersWhisperBot</b> <i>target_user</i> <u>options</u> <code>whisper_text</code>

<b>Description:</b> target user can be either user id or username
any other entity will be failed. To mention more than one target user,
use [ and ] to type target user more than one.
<b><u>e.g</u>:</b> [12345, 67890] (can use with/without , comma.)

<b>[•] You can use <u>options</u> to customize the whisper:</b>
<b>• Options:</b>

<b>---></b> <code>--one-time-open</code>
<b>Description:</b> Targeted user will <b>only</b> able to read the whisper for 1 time.

<b>---></b> <code>--notify-me-on-read</code>
<b>Description:</b> You'll get a message notification in the bot's private, when targeted user(s) opens the whisper message.
<b>Note:</b> You must've messaged bot privately once before, and should unblock the bot (<i>if blocked</i>).
    '''
    ]

go_back_to_start_menu_button_text = [
    'GO BACK TO START MENU'
    ]

inline_whisper_usage_text = [
    *inline_usage_text
    ]

inline_whisper_usage_title = [
    'How to use whisper?'
    ]

inline_whisper_usage_description = [
    'How to use whisper? click here to know!'
    ]

invalid_target_user_mention_title = [
    '• Invalid target user mention'
    ]

invalid_target_user_mention_description = [
    '• The target user you\'re trying to mention is <b>not</b> a correct method.'
    ]

whisper_target_user_invalid_text = [
    'Invalid way of mentiong user...'
    ]

whipser_target_user_not_found_title = [
    '• Target user not found'
    ]

whipser_target_user_not_found_description = [
    '• The target user was not found!'
    ]

whipser_target_user_not_found_text = [
    '• Target User was <b>not</b> found!'
    ]

whipser_target_user_invalid_text = [
    '• <b>Invalid</b> target mention.'
    ]

write_whisper_text_title = [
    'Write your whisper text!'
    ]

write_whisper_text_description = [
    'Write your whisper text after mentioning target user...'
    ]

write_whisper_text = [
    'You should write the whisper text after mentioning target user...'
    ]

multi_target_users_whisper_open_message_text = [
    '''
Dear {},

You all have gotten a Whisper message.

<b>Whisper Message By:</b> {} [<code>{}</code>]

<i>Press the open button below to read the whisper.</i>
    '''
    ]

single_target_user_whisper_open_message_text = [
    '''
Dear {} [<code>{}</code>],

You've gotten a Whisper message.

<b>Whisper Message By:</b> {} [<code>{}</code>]

Click the button below to read the <b>Whisper</b>.
    '''
    ]

whisper_open_message_title = [
    'A Whisper Message!'
    ]

whisper_open_message_description = [
    'A Whisper Message For {}!'
    ]

open_whisper_button_text = [
    'Open the whisper',
    'Read the whisper',
    'Show the whisper'
    ]

this_whisper_is_not_for_you_text = [
    '''
• This whisper is not for you!
    '''
    ]

this_whisper_message_was_not_found_text = [
    'Sorry, this whisper message was not found!'
    ]

target_user_has_read_whisper_text = [
    '''
<b>• </b> <i>Target user</i> has <b>read</b> your whisper message!

<b>Target User:<b> {}

<b>Whisper Text:</b>
<code>{}</code>
    '''
    ]

delete_whisper_message_button_text = [
    'Delete Whisper'
    ]

no_active_whisper_is_avaiable_by_you_text = [
    'No active whisper is avaiable by you.'
    ]

no_whisper_was_found_for_this_targeted_user_to_delete_text = [
    'No whisper text was found for this targeted user {} to delete.'
    ]

callback_target_user_was_not_found_text = [
    '''
• Failed to Delete!

• Target user was not found: {}
    '''
    ]

callback_delete_whispers_text = [
    '''
• Successfully delete whisper(s)!

• Deleted whisper: {}
• Failed to delete whisper: {}
    '''
    ]