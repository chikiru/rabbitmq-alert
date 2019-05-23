#! /usr/bin/python2
# -*- coding: utf8 -*-

import unittest
import mock
from . import rabbitmqalert
from . import optionsresolver


class RabbitMQAlertTestCase(unittest.TestCase):

    def setUp(self):
        rabbitmqalert.urllib2_real = rabbitmqalert.urllib2
        optionsresolver.OptionsResolver.setup_options_real = optionsresolver.OptionsResolver.setup_options

    def tearDown(self):
        rabbitmqalert.urllib2 = rabbitmqalert.urllib2_real
        optionsresolver.OptionsResolver.setup_options = optionsresolver.OptionsResolver.setup_options_real

    def test_check_queue_conditions_not_send_notification_when_not_exceeding_options(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_queue()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_queue_conditions_messages_ready_send_notification_when_exceeding_option(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_queue()
        response["messages_ready"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_messages_unacknowledged_send_notification_when_exceeding_option(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_queue()
        response["messages_unacknowledged"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_messages_send_notification_when_exceeding_option(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_queue()
        response["messages"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_connection_conditions_open_connections_not_send_notification_when_exceeding_option(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_connection()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_connection_conditions_open_connections_send_notification_when_beneath_option(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_connection()
        response.pop("connection_foo")
        response.pop("connection_bar")
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_consumer_conditions_consumers_connected_not_send_notification_when_exceeding_option(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_consumer()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_consumer_conditions_consumers_connected_send_notification_when_beneath_option(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_consumer()
        response.pop("consumer_foo")
        response.pop("consumer_bar")
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_not_send_notification_when_normal(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_node()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_node_conditions_send_notification_when_nodes_running_beneath_option(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_node()
        response.pop()
        response.pop()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_send_notification_when_node_memory_exceeding_option(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        response = self.construct_response_node()
        response[0]["mem_used"] = 2000000
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_get_queues_returns_queues_when_exist(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        response = self.construct_response_queues()
        rmqa.send_request = mock.MagicMock(return_value=response)
        queues = rmqa.get_queues(options)

        logger.info.assert_called_once()
        logger.error.assert_not_called()
        rmqa.send_request.assert_called_once()
        self.assertEquals(["foo", "bar"], queues)

    def test_get_queues_returns_empty_list_when_no_queues_exist(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)

        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        response = self.construct_response_queues_empty()
        rmqa.send_request = mock.MagicMock(return_value=response)
        queues = rmqa.get_queues(options)

        logger.info.assert_not_called()
        logger.error.assert_called_once()
        rmqa.send_request.assert_called_once()
        self.assertEquals([], queues)

    def test_send_notification_sends_email_when_email_to_is_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once()

    def test_send_notification_calls_login_when_email_password_is_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["email_password"] = "password"
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().login.assert_called_once()

    def test_send_notification_does_not_call_login_when_email_password_not_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().login.assert_not_called()

    def test_send_notification_sends_email_with_ssl_when_email_ssl_is_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["email_ssl"] = True
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP_SSL().sendmail.assert_called_once()

    def test_send_notification_does_not_send_email_when_email_to_not_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["email_to"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_not_called()

    def test_send_notification_sends_to_slack_and_telegram_when_options_are_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.urllib2.urlopen.assert_called()

    def test_send_notification_does_not_send_to_slack_when_any_option_not_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["slack_url"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        # Assure only telegram is called
        rabbitmqalert.urllib2.urlopen.assert_called_once()

    def test_send_notification_does_not_send_to_telegram_when_any_option_not_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["telegram_bot_id"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        # Assure only slack is called
        rabbitmqalert.urllib2.urlopen.assert_called_once()

    def test_send_notification_uses_host_alias_when_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once_with('bar@foobar.com', ['foo@foobar.com'], 'Subject: foo bar-host foo\n\nbar-host - ')

    def test_send_notification_does_not_use_host_alias_when_not_set(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["host_alias"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once_with('bar@foobar.com', ['foo@foobar.com'], 'Subject: foo foo-host foo\n\nfoo-host - ')

    def test_send_notification_logs_info_when_email_is_sent(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["slack_url"] = None
        options["telegram_bot_id"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_email_not_sent(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["email_to"] = None
        options["slack_url"] = None
        options["telegram_bot_id"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_not_called()

    def test_send_notification_logs_info_when_sending_to_slack(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["email_to"] = None
        options["telegram_bot_id"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_not_sending_to_slack(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["email_to"] = None
        options["slack_url"] = None
        options["telegram_bot_id"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_not_called()

    def test_send_notification_logs_info_when_sending_to_telegram(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["email_to"] = None
        options["slack_url"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_not_sending_to_telegram(self):
        logger = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger)
        options = self.construct_options()
        options["email_to"] = None
        options["slack_url"] = None
        options["telegram_bot_id"] = None
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_not_called()

    def test_main_runs_check_queue_conditions_when_ready_queue_size_in_queue_conditions(self):
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger)

        options = {
            "queues": ["foo"],
            "generic_conditions": {},
            "check_rate": 1,
            "conditions": {
                "foo": {
                    "ready_queue_size": 1
                }
            }
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_called()
        rmqa.check_node_conditions.assert_not_called()
        rmqa.check_connection_conditions.assert_not_called()
        rmqa.check_consumer_conditions.assert_not_called()

    def test_main_runs_check_queue_conditions_when_unack_queue_size_in_queue_conditions(self):
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger)

        options = {
            "queues": ["foo"],
            "generic_conditions": {},
            "check_rate": 1,
            "conditions": {
                "foo": {
                    "unack_queue_size": 1
                }
            }
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_called()
        rmqa.check_node_conditions.assert_not_called()
        rmqa.check_connection_conditions.assert_not_called()
        rmqa.check_consumer_conditions.assert_not_called()

    def test_main_runs_check_queue_conditions_when_total_queue_size_in_queue_conditions(self):
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger)

        options = {
            "queues": ["foo"],
            "generic_conditions": {},
            "check_rate": 1,
            "conditions": {
                "foo": {
                    "total_queue_size": 1
                }
            }
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_called()
        rmqa.check_node_conditions.assert_not_called()
        rmqa.check_connection_conditions.assert_not_called()
        rmqa.check_consumer_conditions.assert_not_called()

    def test_main_runs_check_queue_conditions_when_queue_consumers_connected_in_queue_conditions(self):
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger)

        options = {
            "queues": ["foo"],
            "generic_conditions": {},
            "check_rate": 1,
            "conditions": {
                "foo": {
                    "queue_consumers_connected": 1
                }
            }
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_called()
        rmqa.check_node_conditions.assert_not_called()
        rmqa.check_connection_conditions.assert_not_called()
        rmqa.check_consumer_conditions.assert_not_called()

    def test_main_runs_check_node_conditions_when_nodes_running_in_generic_conditions(self):
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger)

        options = {
            "queues": [],
            "generic_conditions": {
                "nodes_running": 1
            },
            "check_rate": 1,
            "conditions": {}
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_not_called()
        rmqa.check_node_conditions.assert_called()
        rmqa.check_connection_conditions.assert_not_called()
        rmqa.check_consumer_conditions.assert_not_called()

    def test_main_runs_check_node_conditions_when_node_memory_used_in_generic_conditions(self):
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger)

        options = {
            "queues": [],
            "generic_conditions": {
                "node_memory_used": 1
            },
            "check_rate": 1,
            "conditions": {}
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_not_called()
        rmqa.check_node_conditions.assert_called()
        rmqa.check_connection_conditions.assert_not_called()
        rmqa.check_consumer_conditions.assert_not_called()

    def test_main_runs_check_connection_conditions_when_open_connections_in_generic_conditions(self):
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger)

        options = {
            "queues": [],
            "generic_conditions": {
                "open_connections": 1
            },
            "check_rate": 1,
            "conditions": {}
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_not_called()
        rmqa.check_node_conditions.assert_not_called()
        rmqa.check_connection_conditions.assert_called()
        rmqa.check_consumer_conditions.assert_not_called()

    def test_main_runs_check_consumer_conditions_when_consumers_connected_in_generic_conditions(self):
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger)

        options = {
            "queues": [],
            "generic_conditions": {
                "consumers_connected": 1
            },
            "check_rate": 1,
            "conditions": {}
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_not_called()
        rmqa.check_node_conditions.assert_not_called()
        rmqa.check_connection_conditions.assert_not_called()
        rmqa.check_consumer_conditions.assert_called()

    @staticmethod
    def construct_options():
        options = {
            "scheme": "http",
            "host": "foo-host",
            "port": 1,
            "host_alias": "bar-host",
            "vhost": "foo",
            "queue": "foo",
            "queues": ["foo"],
            "queues_discovery": False,
            "generic_conditions": {
                "ready_queue_size": 0,
                "unack_queue_size": 0,
                "total_queue_size": 0,
                "queue_consumers_connected": 0,
                "consumers_connected": 1,
                "open_connections": 1,
                "nodes_running": 1,
                "node_memory_used": 1
            },
            "conditions": {
                "foo": {
                    "ready_queue_size": 0,
                    "unack_queue_size": 0,
                    "total_queue_size": 0,
                    "queue_consumers_connected": 0,
                    "consumers_connected": 1,
                    "open_connections": 1,
                    "nodes_running": 1,
                    "node_memory_used": 1
                }
            },
            "email_to": ["foo@foobar.com"],
            "email_from": "bar@foobar.com",
            "email_subject": "foo %s %s",
            "email_server": "mail.foobar.com",
            "email_password": "",
            "email_ssl": False,
            "slack_url": "http://foo.com",
            "slack_channel": "channel",
            "slack_username": "username",
            "telegram_bot_id": "foo_bot",
            "telegram_channel": "foo_channel"
        }

        return options

    @staticmethod
    def construct_response_queue():
        return {
            "messages_ready": 0,
            "messages_unacknowledged": 0,
            "messages": 0,
            "consumers": 0
        }

    @staticmethod
    def construct_response_connection():
        return {
            "connection_foo": {},
            "connection_bar": {}
        }

    @staticmethod
    def construct_response_consumer():
        return {
            "consumer_foo": {},
            "consumer_bar": {}
        }

    @staticmethod
    def construct_response_node():
        return [
            { "mem_used": 500000 },
            { "mem_used": 500000 }
        ]

    @staticmethod
    def construct_response_queues():
        return {
            "page_count": 1,
            "page_size": 300,
            "page": 1,
            "filtered_count": 2,
            "item_count": 2,
            "total_count": 2,
            "items": [
                {
                    "name": "foo",
                },
                {
                    "name": "bar",
                }
            ]
        }

    @staticmethod
    def construct_response_queues_empty():
        return {
            "page_count": 1,
            "page_size": 300,
            "page": 1,
            "filtered_count": 0,
            "item_count": 0,
            "total_count": 0,
            "items": []
        }


if __name__ == "__main__":
    unittest.main()
