from telegram import (Bot, KeyboardButton, ReplyKeyboardMarkup,
                      ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import emoji
import logging
import json

from bot.user.User import User

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

UMBRELLAID, LOCATION = range(2)
UPDATE = 0

class RainBot:
    """Class RainBot:
    
    Class implementing our Telegram bot. It takes care of the interaction with
    our Telegram users, by asking them first the ID of their umbrella and if
    they want to share their location. This information is sent to the
    raspberryPI of the user so that it can pair the chat_ID of the user to its
    umbrellaID. Then when the RainBot receives a notification of the BotManager
    it notifies the user whose chat_ID matches the one specified by the
    BotManager.

    Attributes:
        bot (:obj: `telegram.Bot`): instance of our Telegram bot
        updater (:obj: `telegram.ext.Updater`): event handler for our bot
        dp (:obj: `telegram.ext.dispatcher`): dispatcher to which we register
            the different handlers
        usersDB (str): name of the file in which to save the users
    """

    # List of available commands
    cmds = ["/start", "/help", "/update_location", "/update_umbrellaID"]

    # Token of our bot, given by the BotFather
    token = "455874909:AAHH3IgpkvC5Ud3sSmuiNisiU8XhYJ9ypRY"

    # List of users
    users = {}


    def __init__(self, usersDB = None):
        """ Constructor of RainBot:

        Creates and initiates the EventHandler of our bot, register the
        different handlers needed by it to interact with our users and if
        specified it will also retrieve the users who have already used it.
        
        Args:
            usersDB (str): name of the file in which to save the users
        """
        logger.info("Initiating RainBot!")
        self.bot = Bot(RainBot.token)

        # Creating the EventHandler and passing it RainBot's token.
        self.updater = Updater(RainBot.token)

        # Getting the dispatcher to which we register the handlers
        self.dp = self.updater.dispatcher

        # Conversation handler with the states UMBRELLAID and LOCATION,
        # to initialize first connection to the bot
        init_handler = ConversationHandler(
            entry_points=[CommandHandler('start', RainBot.start)],

            states={
                UMBRELLAID: [MessageHandler(Filters.text,
                                            RainBot.set_umbrellaID),
                             CommandHandler('skip', RainBot.skip_umbrellaID)],

                LOCATION: [MessageHandler(Filters.location,
                                          RainBot.set_location),
                           CommandHandler('skip', RainBot.skip_location)]
            },

            fallbacks=[CommandHandler('cancel', RainBot.cancel)]
        )

        # Adding the initialization handler to the dispatcher
        self.dp.add_handler(init_handler)

        # Conversation handler to update user's location
        update_location_handler = ConversationHandler(
            entry_points=[CommandHandler("update_location",
                                         RainBot.update_location)],

            states={
                UPDATE: [MessageHandler(Filters.location, RainBot.get_location)]
            }, 

            fallbacks=[CommandHandler('cancel', RainBot.cancel)]
        )

        # Adding the handler to the dispatcher
        self.dp.add_handler(update_location_handler)

        # Conversation handler to update user's umbrella_ID
        update_umbrellaID_handler = ConversationHandler(
            entry_points=[CommandHandler("update_umbrellaID",
                                         RainBot.update_umbrellaID)],

            states={
                UPDATE: [MessageHandler(Filters.text, RainBot.get_umbrellaID)]
            }, 

            fallbacks=[CommandHandler('cancel', RainBot.cancel)]
        )

        # Adding the handler to the dispatccher
        self.dp.add_handler(update_umbrellaID_handler)

        # Handler for /help command
        self.dp.add_handler(CommandHandler("help", RainBot.help))
        
        # Backdoor to log in terminal the list of users at the instant where
        # this command is received.
        self.dp.add_handler(CommandHandler("debug_users", RainBot.debug_users))

        # For unknown commands
        self.dp.add_handler(MessageHandler(Filters.text, RainBot.unknown))

        # Logging all errors
        self.dp.add_error_handler(RainBot.error)

        self.usersDB = usersDB
        if self.usersDB != None:
            RainBot.users = self.loadUsers()


    def loadUsers(self):
        """ Method to load the users into the RainBot when it is being started
        """
        logger.info("RainBot has loaded its previous users!")


    def saveUsers(self):
        """ Method to save the users when RainBot shuts down
        """
        logger.info("RainBot has saved its users!")


    def start_bot(self):
        """ Method to start the bot by starting to poll the Telegram Bot API
        """
        self.updater.start_polling()
        logger.info("RainBot now operating!")


    def stop(self):
        """ Method to make RainBot shutdown:

        RainBot stops polling the Telegram Bot API and saves its users.
        """
        self.updater.stop()
        self.saveUsers()
        logger.info("RainBot has shut down!")


    def notify(self, chat_ID):
        """ Method to send rain warning messages:

        To the user whose chat_ID matches the one passed as a parameter.

        Args:
            chat_ID (int): representing the chat_ID of the user
        """
        if chat_ID in RainBot.users:
            usr_fname = RainBot.users[chat_ID].first_name
            usr_lname = RainBot.users[chat_ID].last_name
            usr_id = RainBot.users[chat_ID].id
            logger.info("Sending a rain warning to user %s %s (ID: %s)." \
                        % (usr_fname, usr_lname, usr_id))
            msg = "Hey %s, it's raining where you are, don't forget to take " \
                  "your umbrella! :umbrella_with_rain_drops:" % (usr_fname)
            self.bot.send_message(chat_ID, emoji.emojize(msg))


    # Class methods corresponding to the methods to be called by the
    # EventHandler upon interaction with the user:


    def start(bot, update):
        """ /start command:

        The user initiates communication with the bot for the first time.
        We ask her/him to give us her/his umbrella_ID.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        chat_ID = update.message.chat.id
        usr = update.message.from_user

        logger.info("User %s started using RainBot. User's ID: %s, chat_ID: " \
                    "%s." % (usr.name, usr.id, chat_ID))

        # Create a User and put it in our dictionnary
        RainBot.users[chat_ID] = User(usr)

        greetings = "Hi %s! I'm RainBot, your rain assistant! :robot_face: " \
                    ":umbrella_with_rain_drops:\n\nLet's get started! Can "  \
                    "you send me the ID of your umbrella? You can also use " \
                    "/skip if you prefer to do it later." % (usr.first_name)
        greetings = emoji.emojize(greetings)
        update.message.reply_text(greetings)

        return UMBRELLAID


    def set_umbrellaID(bot, update):
        """ method called upon reception of umbrella_ID asked by /start:

        We set the umbrellaID of the user identified in the incoming update.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        chat_ID = update.message.chat.id
        usr = update.message.from_user
        umbrella_ID = update.message.text

        # Setting umbrella_ID of the user
        RainBot.users[chat_ID].setUmbrellaID(umbrella_ID)

        logger.info("Umbrella_ID of user %s (ID: %s): %s" % (usr.name, \
                    usr.id, umbrella_ID))

        keyboard = [[KeyboardButton("send my location", request_location=True)],
                    [KeyboardButton("/skip")]]

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        update.message.reply_text("Great! Now can you send me your location"  \
                                  " please?", reply_markup=reply_markup)
        
        return LOCATION


    def skip_umbrellaID(bot, update):
        """ /skip command:

        If the user decides to skip setting her/his umbrella_ID then we tell
        her/him that she/he will have to do it to start receiving notifications
        and we ask her/him to share her/his location.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        usr = update.message.from_user
        logger.info("User %s (ID: %s) skipped giving umbrella ID step." \
                    % (usr.name, usr.id))

        keyboard = [[KeyboardButton("send my location", request_location=True)],
                    [KeyboardButton("/skip")]]

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        update.message.reply_text(
            "It's okay for now, but don't forget to give me your umbrella "  \
            "ID at some point. Otherwise I won't be able to send you "       \
            "notifications.\n\nNow %s can you send me your location please? "\
            % (usr.first_name), reply_markup=reply_markup)

        return LOCATION


    def update_umbrellaID(bot, update):
        """ /update_umbrellaID command:

        Method called upon reception of command /update_umbrellaID. RainBot
        asks the user to give her/his umbrella_ID.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        chat_ID = update.message.chat.id
        usr = update.message.from_user

        # if unregistered user, nicely asking her/him to run start
        if chat_ID not in RainBot.users:
            logger.info("Unregistered user %s (ID: %s) tried to update " \
                        "her/his umbrella ID." % (usr.name, usr.id))
            msg = "Uh oh, it seems like you haven't run the /start command " \
                  ":confused_face: . Please run it to be able to use this "\
                  "command."
            update.message.reply_text(emoji.emojize(msg))
            return ConversationHandler.END
        
        logger.info("User %s (ID: %s) wants to update her/his umbrella ID." \
                    % (usr.name, usr.id))
        msg = "Sure thing %s, what is the new ID of your umbrella?" \
              % (usr.first_name)
        update.message.reply_text(msg)

        return UPDATE


    def get_umbrellaID(bot, update):
        """ Method called upon reception of umbrella_ID sent by user

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        chat_ID = update.message.chat.id
        usr = update.message.from_user
        umbrella_ID = update.message.text

        # Updating User's umbrella_ID
        RainBot.users[chat_ID].updateUmbrellaID(umbrella_ID)

        logger.info("User %s %s (ID: %s) new umbrella's ID is: %s" \
                    % (usr.first_name, usr.last_name, usr.id, umbrella_ID))
        msg = "Done! Your new umbrella ID is: %s :OK_hand:" % (umbrella_ID)
        update.message.reply_text(emoji.emojize(msg))

        return ConversationHandler.END


    def set_location(bot, update):
        """ Method called upon reception of location asked by set_umbrellaID:

        We set the location of the user identified in the incoming update.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        chat_ID = update.message.chat.id
        usr = update.message.from_user
        usr_loc = update.message.location

        # Setting User's location
        RainBot.users[chat_ID].setLocation(usr_loc)

        logger.info("Location of user %s (ID: %s): lat: %f / long: %f" \
                    % (usr.name, usr.id, usr_loc.latitude, usr_loc.longitude))
        msg = "Awesome %s! We're now all set! :OK_hand:" % (usr.first_name)
        update.message.reply_text(emoji.emojize(msg),
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END


    def skip_location(bot, update):
        """ /skip command:

        If the user skips the step where she/he shares her/his location then
        we remind her/him to do so to start receiving notifications and we
        finish initialization.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        usr = update.message.from_user
        logger.info("User %s %s (ID: %s) did not send a location." \
                    % (usr.first_name, usr.last_name, usr.id))
        update.message.reply_text("It's okay for now, but don't forget to "\
                                  "give me your location at some point. "\
                                  "Otherwise I won't be able to send you "\
                                  "notifications. To do so use command: "\
                                  "/update_location",\
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END


    def update_location(bot, update):
        """ /update_location:

        Method called upon reception of /update_location by RainBot by which
        user expresses her/his wish to update its location. Therefore, we ask
        her her/him to share his location.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        chat_ID = update.message.chat.id
        usr = update.message.from_user

        # if unregistered user, nicely asking her/him to run start
        if chat_ID not in RainBot.users:
            logger.info("Unregistered user %s (ID: %s) tried to update " \
                        "her/his location." % (usr.name, usr.id))
            msg = "Uh oh, it seems like you haven't run the /start command " \
                  ":confused_face: . Please run it to be able to use this "\
                  "command."
            update.message.reply_text(emoji.emojize(msg))
            return ConversationHandler.END

        logger.info("User %s %s (ID: %s) wants to update her/his location." \
                    % (usr.first_name, usr.last_name, usr.id))
        msg = "Sure thing %s, what is your new location?" % (usr.first_name)

        keyboard = [[KeyboardButton("send my location", request_location=True)]]

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        update.message.reply_text(msg, reply_markup=reply_markup)

        return UPDATE


    def get_location(bot, update):
        """ method called upon reception of user's location by RainBot:

        When user has asked to update her/his location.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        chat_ID = update.message.chat.id
        usr = update.message.from_user
        usr_loc = update.message.location

        # Updating User's location
        RainBot.users[chat_ID].setLocation(usr_loc)

        logger.info("New location of user %s %s (ID: %s): lat: %f / long: %f" \
                    % (usr.first_name, usr.last_name, usr.id, \
                       usr_loc.latitude, usr_loc.longitude))
        msg = "Done! Your location has been updated! :OK_hand:"
        update.message.reply_text(emoji.emojize(msg), \
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END


    def cancel(bot, update):
        """ /cancel command:

        Method that is called upon reception of command /cancel by RainBot.
        This command can be issued by the user at any point during
        initialization and update phases to quit the process.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        user = update.message.from_user
        logger.info("User %s %s (ID: %s) quit umbrella_ID and location "\
                    "initialization" % (usr.first_name, usr.last_name, usr.id))
        update.message.reply_text("Ok %s, let's get started next time!"\
                                  % (usr.first_name), \
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END


    def help(bot, update):
        """ /help command:

        Method called upon reception of command /cancel by RainBot. It sends
        the user a list of command to use.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        usr = update.message.from_user
        logger.info("User %s %s (ID: %s) just asked for help." \
                    % (usr.first_name, usr.last_name, usr.id))
        msg = "Coming to your help!\n"
        msg += "Here's the list of avaible commands:\n"
        for cmd in RainBot.cmds:
            msg += "- " + str(cmd) + "\n"
        update.message.reply_text(msg)


    def unknown(bot, update):
        """ Method called upon reception of unknown command or message:

        It can happen if user tries to write to RainBot or uses an unrecognized
        command.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        usr = update.message.from_user
        logger.info("User %s %s (ID: %s) just made an unknown command." \
                    % (usr.first_name, usr.last_name, usr.id))
        msg = "Sorry %s, I didn't understand that command... :confused_face:" \
              % (usr.first_name)
        update.message.reply_text(emoji.emojize(msg))


    def debug_users(bot, update):
        """ /debug_users command:

        Method called upon reception of command /debug_users. It will log in
        the terminal the list of the users using the Bot (that have started the
        bot). It will send to the user the same message as when an unknown
        command is received.

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
        """
        users = "List of users:\n"
        for ID in RainBot.users:
            users += "- " + str(RainBot.users[ID])
        logger.info(users)
        RainBot.unknown(bot, update)

    def error(bot, update, error):
        """ Method called upon reception of update that lead to an error

        Args:
            bot (:obj: `telegram.Bot`): bot representing RainBot
            update (:obj: `telegram.Update`): incoming update
            error (:obj: `telegram.error`): error caused by incoming update
        """
        logger.warning('Update "%s" caused error "%s"', update, error)
        