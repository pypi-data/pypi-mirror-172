from __future__ import annotations

import typing
import lapidary_base
import pydantic
import datetime
import gsmtasks.components.schemas.account
import gsmtasks.components.schemas.account_owner_change
import gsmtasks.components.schemas.account_role
import gsmtasks.components.schemas.account_role_activation
import gsmtasks.components.schemas.account_role_token
import gsmtasks.components.schemas.account_stripe_payment_method_attach
import gsmtasks.components.schemas.account_stripe_payment_method_detach
import gsmtasks.components.schemas.account_stripe_payment_method_get
import gsmtasks.components.schemas.account_stripe_payment_method_set_default
import gsmtasks.components.schemas.account_stripe_payment_methods
import gsmtasks.components.schemas.account_stripe_setup_attempt_get
import gsmtasks.components.schemas.account_stripe_setup_intent_create
import gsmtasks.components.schemas.account_stripe_setup_intent_get
import gsmtasks.components.schemas.account_stripe_setup_intents_get
import gsmtasks.components.schemas.account_user
import gsmtasks.components.schemas.addon
import gsmtasks.components.schemas.auth_token
import gsmtasks.components.schemas.authenticated_user_create
import gsmtasks.components.schemas.authenticated_user_update
import gsmtasks.components.schemas.braintree_customer
import gsmtasks.components.schemas.braintree_transaction
import gsmtasks.components.schemas.client
import gsmtasks.components.schemas.client_role
import gsmtasks.components.schemas.configuration_serializer_v2
import gsmtasks.components.schemas.contact_address
import gsmtasks.components.schemas.contact_address_background_import
import gsmtasks.components.schemas.contact_address_export
import gsmtasks.components.schemas.dashboard_scene
import gsmtasks.components.schemas.device
import gsmtasks.components.schemas.document
import gsmtasks.components.schemas.email
import gsmtasks.components.schemas.export
import gsmtasks.components.schemas.form_rule
import gsmtasks.components.schemas.gsm_tasks_error
import gsmtasks.components.schemas.import_mapping
import gsmtasks.components.schemas.integration_request
import gsmtasks.components.schemas.invoice
import gsmtasks.components.schemas.metafield
import gsmtasks.components.schemas.notification
import gsmtasks.components.schemas.notification_template
import gsmtasks.components.schemas.on_duty
import gsmtasks.components.schemas.order_list_scene
import gsmtasks.components.schemas.order_serializer_v2
import gsmtasks.components.schemas.password_change
import gsmtasks.components.schemas.password_reset
import gsmtasks.components.schemas.password_reset_confirm
import gsmtasks.components.schemas.push_notification
import gsmtasks.components.schemas.readable_user
import gsmtasks.components.schemas.recurrence
import gsmtasks.components.schemas.recurrence_list_scene
import gsmtasks.components.schemas.registration
import gsmtasks.components.schemas.render_request
import gsmtasks.components.schemas.review
import gsmtasks.components.schemas.route
import gsmtasks.components.schemas.route_optimization_serializer_v2
import gsmtasks.components.schemas.s3_file_upload
import gsmtasks.components.schemas.signature
import gsmtasks.components.schemas.sms
import gsmtasks.components.schemas.stripe_payment
import gsmtasks.components.schemas.task_account_change
import gsmtasks.components.schemas.task_action
import gsmtasks.components.schemas.task_address_feature
import gsmtasks.components.schemas.task_assign
import gsmtasks.components.schemas.task_command
import gsmtasks.components.schemas.task_event_serializer_v2
import gsmtasks.components.schemas.task_event_track
import gsmtasks.components.schemas.task_export
import gsmtasks.components.schemas.task_form
import gsmtasks.components.schemas.task_list_ext
import gsmtasks.components.schemas.task_list_reorder_request
import gsmtasks.components.schemas.task_list_scene
import gsmtasks.components.schemas.task_metadata
import gsmtasks.components.schemas.task_serializer_v2
import gsmtasks.components.schemas.tasks_background_import
import gsmtasks.components.schemas.tasks_states_count_response
import gsmtasks.components.schemas.time_location
import gsmtasks.components.schemas.time_location_feature
import gsmtasks.components.schemas.tracker
import gsmtasks.components.schemas.validation_error
import gsmtasks.components.schemas.webhook
import gsmtasks.components.schemas.worker_feature
import gsmtasks.components.schemas.worker_track
import gsmtasks.components.schemas.working_state
import gsmtasks.paths.account_roles_activate_create.param_model
import gsmtasks.paths.account_roles_create.param_model
import gsmtasks.paths.account_roles_destroy.param_model
import gsmtasks.paths.account_roles_list.param_model
import gsmtasks.paths.account_roles_notify_create.param_model
import gsmtasks.paths.account_roles_partial_update.param_model
import gsmtasks.paths.account_roles_retrieve.param_model
import gsmtasks.paths.account_roles_token_retrieve.param_model
import gsmtasks.paths.account_roles_update.param_model
import gsmtasks.paths.accounts_braintree_customer_retrieve.param_model
import gsmtasks.paths.accounts_change_owner_create.param_model
import gsmtasks.paths.accounts_list.param_model
import gsmtasks.paths.accounts_managers_create.param_model
import gsmtasks.paths.accounts_managers_destroy.param_model
import gsmtasks.paths.accounts_managers_retrieve.param_model
import gsmtasks.paths.accounts_partial_update.param_model
import gsmtasks.paths.accounts_retrieve.param_model
import gsmtasks.paths.accounts_stripe_attach_payment_method_update.param_model
import gsmtasks.paths.accounts_stripe_create_setup_intent_create.param_model
import gsmtasks.paths.accounts_stripe_create_setup_intent_update.param_model
import gsmtasks.paths.accounts_stripe_detach_payment_method_update.param_model
import gsmtasks.paths.accounts_stripe_get_payment_method_retrieve.param_model
import gsmtasks.paths.accounts_stripe_get_setup_attempt_retrieve.param_model
import gsmtasks.paths.accounts_stripe_get_setup_intent_retrieve.param_model
import gsmtasks.paths.accounts_stripe_payment_methods_retrieve.param_model
import gsmtasks.paths.accounts_stripe_set_default_payment_method_update.param_model
import gsmtasks.paths.accounts_stripe_setup_intents_retrieve.param_model
import gsmtasks.paths.accounts_update.param_model
import gsmtasks.paths.accounts_workers_create.param_model
import gsmtasks.paths.accounts_workers_destroy.param_model
import gsmtasks.paths.accounts_workers_retrieve.param_model
import gsmtasks.paths.addons_list.param_model
import gsmtasks.paths.addons_retrieve.param_model
import gsmtasks.paths.billing_customers_client_token_retrieve.param_model
import gsmtasks.paths.billing_customers_create.param_model
import gsmtasks.paths.billing_customers_list.param_model
import gsmtasks.paths.billing_customers_partial_update.param_model
import gsmtasks.paths.billing_customers_retrieve.param_model
import gsmtasks.paths.billing_customers_update.param_model
import gsmtasks.paths.billing_invoices_list.param_model
import gsmtasks.paths.billing_invoices_mark_as_paid_create.param_model
import gsmtasks.paths.billing_invoices_partial_update.param_model
import gsmtasks.paths.billing_invoices_retrieve.param_model
import gsmtasks.paths.billing_invoices_update.param_model
import gsmtasks.paths.billing_stripe_payments_list.param_model
import gsmtasks.paths.billing_stripe_payments_retrieve.param_model
import gsmtasks.paths.billing_transactions_list.param_model
import gsmtasks.paths.billing_transactions_retrieve.param_model
import gsmtasks.paths.client_roles_create.param_model
import gsmtasks.paths.client_roles_list.param_model
import gsmtasks.paths.client_roles_notify_create.param_model
import gsmtasks.paths.client_roles_partial_update.param_model
import gsmtasks.paths.client_roles_retrieve.param_model
import gsmtasks.paths.client_roles_update.param_model
import gsmtasks.paths.clients_create.param_model
import gsmtasks.paths.clients_list.param_model
import gsmtasks.paths.clients_partial_update.param_model
import gsmtasks.paths.clients_retrieve.param_model
import gsmtasks.paths.clients_update.param_model
import gsmtasks.paths.configurations_list.param_model
import gsmtasks.paths.contact_address_exports_list.param_model
import gsmtasks.paths.contact_address_import_create.param_model
import gsmtasks.paths.contact_address_import_list.param_model
import gsmtasks.paths.contact_address_import_retrieve.param_model
import gsmtasks.paths.contact_addresses_create.param_model
import gsmtasks.paths.contact_addresses_list.param_model
import gsmtasks.paths.contact_addresses_partial_update.param_model
import gsmtasks.paths.contact_addresses_retrieve.param_model
import gsmtasks.paths.contact_addresses_update.param_model
import gsmtasks.paths.devices_create.param_model
import gsmtasks.paths.devices_list.param_model
import gsmtasks.paths.devices_retrieve.param_model
import gsmtasks.paths.docs_schema_retrieve.param_model
import gsmtasks.paths.docs_schema_retrieve.response_body
import gsmtasks.paths.documents_batch_delete_create.param_model
import gsmtasks.paths.documents_create.param_model
import gsmtasks.paths.documents_destroy.param_model
import gsmtasks.paths.documents_list.param_model
import gsmtasks.paths.documents_retrieve.param_model
import gsmtasks.paths.emails_create.param_model
import gsmtasks.paths.emails_destroy.param_model
import gsmtasks.paths.emails_list.param_model
import gsmtasks.paths.emails_partial_update.param_model
import gsmtasks.paths.emails_resend_create.param_model
import gsmtasks.paths.emails_retrieve.param_model
import gsmtasks.paths.emails_update.param_model
import gsmtasks.paths.exports_create.param_model
import gsmtasks.paths.exports_destroy.param_model
import gsmtasks.paths.exports_list.param_model
import gsmtasks.paths.exports_partial_update.param_model
import gsmtasks.paths.exports_retrieve.param_model
import gsmtasks.paths.exports_update.param_model
import gsmtasks.paths.file_uploads_create.param_model
import gsmtasks.paths.file_uploads_list.param_model
import gsmtasks.paths.file_uploads_retrieve.param_model
import gsmtasks.paths.formrules_create.param_model
import gsmtasks.paths.formrules_destroy.param_model
import gsmtasks.paths.formrules_list.param_model
import gsmtasks.paths.formrules_partial_update.param_model
import gsmtasks.paths.formrules_retrieve.param_model
import gsmtasks.paths.formrules_update.param_model
import gsmtasks.paths.integrations_create.param_model
import gsmtasks.paths.metafields_create.param_model
import gsmtasks.paths.metafields_destroy.param_model
import gsmtasks.paths.metafields_list.param_model
import gsmtasks.paths.metafields_partial_update.param_model
import gsmtasks.paths.metafields_retrieve.param_model
import gsmtasks.paths.metafields_update.param_model
import gsmtasks.paths.notification_templates_create.param_model
import gsmtasks.paths.notification_templates_destroy.param_model
import gsmtasks.paths.notification_templates_list.param_model
import gsmtasks.paths.notification_templates_partial_update.param_model
import gsmtasks.paths.notification_templates_render_create.param_model
import gsmtasks.paths.notification_templates_retrieve.param_model
import gsmtasks.paths.notification_templates_update.param_model
import gsmtasks.paths.notifications_create.param_model
import gsmtasks.paths.notifications_list.param_model
import gsmtasks.paths.notifications_retrieve.param_model
import gsmtasks.paths.password_change_create.param_model
import gsmtasks.paths.password_reset_confirm_create.param_model
import gsmtasks.paths.password_reset_create.param_model
import gsmtasks.paths.push_notifications_create.param_model
import gsmtasks.paths.push_notifications_destroy.param_model
import gsmtasks.paths.push_notifications_list.param_model
import gsmtasks.paths.push_notifications_partial_update.param_model
import gsmtasks.paths.push_notifications_resend_create.param_model
import gsmtasks.paths.push_notifications_retrieve.param_model
import gsmtasks.paths.push_notifications_update.param_model
import gsmtasks.paths.register_create.param_model
import gsmtasks.paths.reports_tasks_states_count_retrieve.param_model
import gsmtasks.paths.reviews_create.param_model
import gsmtasks.paths.reviews_list.param_model
import gsmtasks.paths.reviews_retrieve.param_model
import gsmtasks.paths.route_optimizations_commit_create.param_model
import gsmtasks.paths.route_optimizations_create.param_model
import gsmtasks.paths.route_optimizations_list.param_model
import gsmtasks.paths.route_optimizations_results_retrieve.param_model
import gsmtasks.paths.route_optimizations_retrieve.param_model
import gsmtasks.paths.route_optimizations_routes_create.param_model
import gsmtasks.paths.route_optimizations_routes_retrieve.param_model
import gsmtasks.paths.route_optimizations_schedule_create.param_model
import gsmtasks.paths.scenes_dashboard_list.param_model
import gsmtasks.paths.scenes_task_list_list.param_model
import gsmtasks.paths.signatures_batch_delete_create.param_model
import gsmtasks.paths.signatures_create.param_model
import gsmtasks.paths.signatures_destroy.param_model
import gsmtasks.paths.signatures_list.param_model
import gsmtasks.paths.signatures_retrieve.param_model
import gsmtasks.paths.sms_create.param_model
import gsmtasks.paths.sms_destroy.param_model
import gsmtasks.paths.sms_list.param_model
import gsmtasks.paths.sms_partial_update.param_model
import gsmtasks.paths.sms_resend_create.param_model
import gsmtasks.paths.sms_retrieve.param_model
import gsmtasks.paths.sms_update.param_model
import gsmtasks.paths.task_address_features_list.param_model
import gsmtasks.paths.task_address_features_retrieve.param_model
import gsmtasks.paths.task_commands_create.param_model
import gsmtasks.paths.task_commands_list.param_model
import gsmtasks.paths.task_commands_retrieve.param_model
import gsmtasks.paths.task_commands_update.param_model
import gsmtasks.paths.task_event_tracks_list.param_model
import gsmtasks.paths.task_event_tracks_retrieve.param_model
import gsmtasks.paths.task_events_list.param_model
import gsmtasks.paths.task_events_retrieve.param_model
import gsmtasks.paths.task_exports_list.param_model
import gsmtasks.paths.task_forms_create.param_model
import gsmtasks.paths.task_forms_destroy.param_model
import gsmtasks.paths.task_forms_list.param_model
import gsmtasks.paths.task_forms_partial_update.param_model
import gsmtasks.paths.task_forms_retrieve.param_model
import gsmtasks.paths.task_forms_update.param_model
import gsmtasks.paths.task_import_create.param_model
import gsmtasks.paths.task_import_list.param_model
import gsmtasks.paths.task_import_mapping_create.param_model
import gsmtasks.paths.task_import_mapping_list.param_model
import gsmtasks.paths.task_import_mapping_retrieve.param_model
import gsmtasks.paths.task_import_retrieve.param_model
import gsmtasks.paths.task_metadatas_list.param_model
import gsmtasks.paths.task_metadatas_retrieve.param_model
import gsmtasks.paths.tasks_accept_create.param_model
import gsmtasks.paths.tasks_account_change_create.param_model
import gsmtasks.paths.tasks_activate_create.param_model
import gsmtasks.paths.tasks_assign_create.param_model
import gsmtasks.paths.tasks_cancel_create.param_model
import gsmtasks.paths.tasks_complete_create.param_model
import gsmtasks.paths.tasks_create.param_model
import gsmtasks.paths.tasks_documents_retrieve.param_model
import gsmtasks.paths.tasks_events_retrieve.param_model
import gsmtasks.paths.tasks_fail_create.param_model
import gsmtasks.paths.tasks_list.param_model
import gsmtasks.paths.tasks_partial_update.param_model
import gsmtasks.paths.tasks_reject_create.param_model
import gsmtasks.paths.tasks_reorder_create.param_model
import gsmtasks.paths.tasks_reposition_create.param_model
import gsmtasks.paths.tasks_retrieve.param_model
import gsmtasks.paths.tasks_signatures_retrieve.param_model
import gsmtasks.paths.tasks_transit_create.param_model
import gsmtasks.paths.tasks_unaccept_create.param_model
import gsmtasks.paths.tasks_unassign_create.param_model
import gsmtasks.paths.tasks_update.param_model
import gsmtasks.paths.time_location_features_create.param_model
import gsmtasks.paths.time_location_features_destroy.param_model
import gsmtasks.paths.time_location_features_list.param_model
import gsmtasks.paths.time_location_features_partial_update.param_model
import gsmtasks.paths.time_location_features_retrieve.param_model
import gsmtasks.paths.time_location_features_update.param_model
import gsmtasks.paths.time_locations_create.param_model
import gsmtasks.paths.time_locations_list.param_model
import gsmtasks.paths.time_locations_retrieve.param_model
import gsmtasks.paths.trackers_create.param_model
import gsmtasks.paths.trackers_list.param_model
import gsmtasks.paths.trackers_partial_update.param_model
import gsmtasks.paths.trackers_public_retrieve.param_model
import gsmtasks.paths.trackers_retrieve.param_model
import gsmtasks.paths.trackers_update.param_model
import gsmtasks.paths.users_activate_create.param_model
import gsmtasks.paths.users_create.param_model
import gsmtasks.paths.users_destroy.param_model
import gsmtasks.paths.users_list.param_model
import gsmtasks.paths.users_on_duty_destroy.param_model
import gsmtasks.paths.users_on_duty_log_create.param_model
import gsmtasks.paths.users_on_duty_log_list.param_model
import gsmtasks.paths.users_on_duty_log_retrieve.param_model
import gsmtasks.paths.users_on_duty_retrieve.param_model
import gsmtasks.paths.users_on_duty_update.param_model
import gsmtasks.paths.users_partial_update.param_model
import gsmtasks.paths.users_retrieve.param_model
import gsmtasks.paths.users_update.param_model
import gsmtasks.paths.webhooks_active_create.param_model
import gsmtasks.paths.webhooks_create.param_model
import gsmtasks.paths.webhooks_destroy.param_model
import gsmtasks.paths.webhooks_inactive_create.param_model
import gsmtasks.paths.webhooks_list.param_model
import gsmtasks.paths.webhooks_partial_update.param_model
import gsmtasks.paths.webhooks_retrieve.param_model
import gsmtasks.paths.webhooks_update.param_model
import gsmtasks.paths.worker_features_list.param_model
import gsmtasks.paths.worker_features_retrieve.param_model
import gsmtasks.paths.worker_tracks_list.param_model
import gsmtasks.paths.working_state_create.param_model
import gsmtasks.paths.working_state_list.param_model
import gsmtasks.paths.working_state_retrieve.param_model
import httpx
import lapidary_base
import lapidary_base.absent
import typing
import uuid


class ApiClient(lapidary_base.ApiBase):
    def __init__(
        self,
        tokenAuth_authorization: str,
        base_url="https://api.gsmtasks.com/",
    ):
        super().__init__(
            client=httpx.AsyncClient(base_url=base_url, headers=[]),
            global_response_map={
                "400": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.validation_error.ValidationError,
                },
                "4XX": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.gsm_tasks_error.GSMTasksError,
                },
                "5XX": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.gsm_tasks_error.GSMTasksError,
                },
            },
        )
        self.auth_tokenAuth = lapidary_base.ApiKeyAuth(
            name="Authorization",
            api_key=tokenAuth_authorization,
            placement=lapidary_base.ParamPlacement.header,
            value_prefix="Token ",
        )

    async def __aenter__(self) -> "ApiClient":
        return await super().__aenter__()

    async def account_roles_activate_create(
        self,
        request_body: gsmtasks.components.schemas.account_role_activation.AccountRoleActivation,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.account_roles_activate_create.param_model.AccountRolesActivateCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_role_activation.AccountRoleActivation:
        import gsmtasks.paths.account_roles_activate_create.param_model

        param_model = gsmtasks.paths.account_roles_activate_create.param_model.AccountRolesActivateCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/account_roles/{p_id}/activate/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_role_activation.AccountRoleActivation,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.account_role_activation.AccountRoleActivation,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def account_roles_create(
        self,
        request_body: gsmtasks.components.schemas.account_role.AccountRole,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.account_roles_create.param_model.AccountRolesCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_role.AccountRole:
        import gsmtasks.paths.account_roles_create.param_model

        param_model = (
            gsmtasks.paths.account_roles_create.param_model.AccountRolesCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/account_roles/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def account_roles_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.account_roles_destroy.param_model.AccountRolesDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.account_roles_destroy.param_model

        param_model = (
            gsmtasks.paths.account_roles_destroy.param_model.AccountRolesDestroy(
                **locals()
            )
        )
        return await super()._request(
            "DELETE",
            f"/account_roles/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def account_roles_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_activated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_deleted_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_display_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.account_roles_list.param_model.AccountRolesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_active: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_integration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_manager: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_worker: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.account_roles_list.param_model.AccountRolesListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.account_role.AccountRole,]:
        import gsmtasks.paths.account_roles_list.param_model

        param_model = gsmtasks.paths.account_roles_list.param_model.AccountRolesList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/account_roles/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.account_role.AccountRole
                    ],
                    "application/xml; version=2.4.11": list[
                        gsmtasks.components.schemas.account_role.AccountRole
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def account_roles_notify_create(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.account_roles_notify_create.param_model.AccountRolesNotifyCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_role.AccountRole:
        import gsmtasks.paths.account_roles_notify_create.param_model

        param_model = gsmtasks.paths.account_roles_notify_create.param_model.AccountRolesNotifyCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/account_roles/{p_id}/notify/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def account_roles_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_account_role.PatchedAccountRole,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.account_roles_partial_update.param_model.AccountRolesPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_role.AccountRole:
        import gsmtasks.paths.account_roles_partial_update.param_model

        param_model = gsmtasks.paths.account_roles_partial_update.param_model.AccountRolesPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/account_roles/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def account_roles_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.account_roles_retrieve.param_model.AccountRolesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_role.AccountRole:
        import gsmtasks.paths.account_roles_retrieve.param_model

        param_model = (
            gsmtasks.paths.account_roles_retrieve.param_model.AccountRolesRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/account_roles/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def account_roles_token_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.account_roles_token_retrieve.param_model.AccountRolesTokenRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_role_token.AccountRoleToken:
        import gsmtasks.paths.account_roles_token_retrieve.param_model

        param_model = gsmtasks.paths.account_roles_token_retrieve.param_model.AccountRolesTokenRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/account_roles/{p_id}/token/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_role_token.AccountRoleToken,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.account_role_token.AccountRoleToken,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def account_roles_update(
        self,
        request_body: gsmtasks.components.schemas.account_role.AccountRole,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.account_roles_update.param_model.AccountRolesUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_role.AccountRole:
        import gsmtasks.paths.account_roles_update.param_model

        param_model = (
            gsmtasks.paths.account_roles_update.param_model.AccountRolesUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PUT",
            f"/account_roles/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.account_role.AccountRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_braintree_customer_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_braintree_customer_retrieve.param_model.AccountsBraintreeCustomerRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account.Account:
        import gsmtasks.paths.accounts_braintree_customer_retrieve.param_model

        param_model = gsmtasks.paths.accounts_braintree_customer_retrieve.param_model.AccountsBraintreeCustomerRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/accounts/{p_id}/braintree_customer/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account.Account,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account.Account,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_change_owner_create(
        self,
        request_body: gsmtasks.components.schemas.account_owner_change.AccountOwnerChange,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_change_owner_create.param_model.AccountsChangeOwnerCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_owner_change.AccountOwnerChange:
        import gsmtasks.paths.accounts_change_owner_create.param_model

        param_model = gsmtasks.paths.accounts_change_owner_create.param_model.AccountsChangeOwnerCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/accounts/{p_id}/change_owner/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_owner_change.AccountOwnerChange,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_owner_change.AccountOwnerChange,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.accounts_list.param_model.AccountsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.account.Account,]:
        import gsmtasks.paths.accounts_list.param_model

        param_model = gsmtasks.paths.accounts_list.param_model.AccountsList(**locals())
        return await super()._request(
            "GET",
            f"/accounts/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.account.Account
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.account.Account
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_managers_create(
        self,
        request_body: gsmtasks.components.schemas.account_user.AccountUser,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_managers_create.param_model.AccountsManagersCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_user.AccountUser:
        import gsmtasks.paths.accounts_managers_create.param_model

        param_model = (
            gsmtasks.paths.accounts_managers_create.param_model.AccountsManagersCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/accounts/{p_id}/managers/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_user.AccountUser,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_user.AccountUser,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_managers_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_managers_destroy.param_model.AccountsManagersDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.accounts_managers_destroy.param_model

        param_model = gsmtasks.paths.accounts_managers_destroy.param_model.AccountsManagersDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/accounts/{p_id}/managers/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def accounts_managers_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_managers_retrieve.param_model.AccountsManagersRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_user.AccountUser:
        import gsmtasks.paths.accounts_managers_retrieve.param_model

        param_model = gsmtasks.paths.accounts_managers_retrieve.param_model.AccountsManagersRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/accounts/{p_id}/managers/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_user.AccountUser,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_user.AccountUser,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_account.PatchedAccount,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_partial_update.param_model.AccountsPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account.Account:
        import gsmtasks.paths.accounts_partial_update.param_model

        param_model = (
            gsmtasks.paths.accounts_partial_update.param_model.AccountsPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/accounts/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account.Account,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account.Account,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_retrieve.param_model.AccountsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account.Account:
        import gsmtasks.paths.accounts_retrieve.param_model

        param_model = gsmtasks.paths.accounts_retrieve.param_model.AccountsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/accounts/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account.Account,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account.Account,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_attach_payment_method_update(
        self,
        request_body: gsmtasks.components.schemas.account_stripe_payment_method_attach.AccountStripePaymentMethodAttach,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_attach_payment_method_update.param_model.AccountsStripeAttachPaymentMethodUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_payment_method_attach.AccountStripePaymentMethodAttach:
        import gsmtasks.paths.accounts_stripe_attach_payment_method_update.param_model

        param_model = gsmtasks.paths.accounts_stripe_attach_payment_method_update.param_model.AccountsStripeAttachPaymentMethodUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/accounts/{p_id}/stripe_attach_payment_method/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_method_attach.AccountStripePaymentMethodAttach,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_method_attach.AccountStripePaymentMethodAttach,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_create_setup_intent_create(
        self,
        request_body: gsmtasks.components.schemas.account_stripe_setup_intent_create.AccountStripeSetupIntentCreate,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_create_setup_intent_create.param_model.AccountsStripeCreateSetupIntentCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_setup_intent_create.AccountStripeSetupIntentCreate:
        import gsmtasks.paths.accounts_stripe_create_setup_intent_create.param_model

        param_model = gsmtasks.paths.accounts_stripe_create_setup_intent_create.param_model.AccountsStripeCreateSetupIntentCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/accounts/{p_id}/stripe_create_setup_intent/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_intent_create.AccountStripeSetupIntentCreate,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_intent_create.AccountStripeSetupIntentCreate,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_create_setup_intent_update(
        self,
        request_body: gsmtasks.components.schemas.account_stripe_setup_intent_create.AccountStripeSetupIntentCreate,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_create_setup_intent_update.param_model.AccountsStripeCreateSetupIntentUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_setup_intent_create.AccountStripeSetupIntentCreate:
        import gsmtasks.paths.accounts_stripe_create_setup_intent_update.param_model

        param_model = gsmtasks.paths.accounts_stripe_create_setup_intent_update.param_model.AccountsStripeCreateSetupIntentUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/accounts/{p_id}/stripe_create_setup_intent/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_intent_create.AccountStripeSetupIntentCreate,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_intent_create.AccountStripeSetupIntentCreate,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_detach_payment_method_update(
        self,
        request_body: gsmtasks.components.schemas.account_stripe_payment_method_detach.AccountStripePaymentMethodDetach,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_detach_payment_method_update.param_model.AccountsStripeDetachPaymentMethodUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_payment_method_detach.AccountStripePaymentMethodDetach:
        import gsmtasks.paths.accounts_stripe_detach_payment_method_update.param_model

        param_model = gsmtasks.paths.accounts_stripe_detach_payment_method_update.param_model.AccountsStripeDetachPaymentMethodUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/accounts/{p_id}/stripe_detach_payment_method/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_method_detach.AccountStripePaymentMethodDetach,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_method_detach.AccountStripePaymentMethodDetach,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_get_payment_method_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_get_payment_method_retrieve.param_model.AccountsStripeGetPaymentMethodRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_payment_method_get.AccountStripePaymentMethodGet:
        import gsmtasks.paths.accounts_stripe_get_payment_method_retrieve.param_model

        param_model = gsmtasks.paths.accounts_stripe_get_payment_method_retrieve.param_model.AccountsStripeGetPaymentMethodRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/accounts/{p_id}/stripe_get_payment_method/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_method_get.AccountStripePaymentMethodGet,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_method_get.AccountStripePaymentMethodGet,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_get_setup_attempt_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_get_setup_attempt_retrieve.param_model.AccountsStripeGetSetupAttemptRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_setup_attempt_get.AccountStripeSetupAttemptGet:
        import gsmtasks.paths.accounts_stripe_get_setup_attempt_retrieve.param_model

        param_model = gsmtasks.paths.accounts_stripe_get_setup_attempt_retrieve.param_model.AccountsStripeGetSetupAttemptRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/accounts/{p_id}/stripe_get_setup_attempt/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_attempt_get.AccountStripeSetupAttemptGet,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_attempt_get.AccountStripeSetupAttemptGet,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_get_setup_intent_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_get_setup_intent_retrieve.param_model.AccountsStripeGetSetupIntentRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_setup_intent_get.AccountStripeSetupIntentGet:
        import gsmtasks.paths.accounts_stripe_get_setup_intent_retrieve.param_model

        param_model = gsmtasks.paths.accounts_stripe_get_setup_intent_retrieve.param_model.AccountsStripeGetSetupIntentRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/accounts/{p_id}/stripe_get_setup_intent/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_intent_get.AccountStripeSetupIntentGet,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_intent_get.AccountStripeSetupIntentGet,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_payment_methods_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_payment_methods_retrieve.param_model.AccountsStripePaymentMethodsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_payment_methods.AccountStripePaymentMethods:
        import gsmtasks.paths.accounts_stripe_payment_methods_retrieve.param_model

        param_model = gsmtasks.paths.accounts_stripe_payment_methods_retrieve.param_model.AccountsStripePaymentMethodsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/accounts/{p_id}/stripe_payment_methods/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_methods.AccountStripePaymentMethods,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_methods.AccountStripePaymentMethods,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_set_default_payment_method_update(
        self,
        request_body: gsmtasks.components.schemas.account_stripe_payment_method_set_default.AccountStripePaymentMethodSetDefault,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_set_default_payment_method_update.param_model.AccountsStripeSetDefaultPaymentMethodUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_payment_method_set_default.AccountStripePaymentMethodSetDefault:
        import gsmtasks.paths.accounts_stripe_set_default_payment_method_update.param_model

        param_model = gsmtasks.paths.accounts_stripe_set_default_payment_method_update.param_model.AccountsStripeSetDefaultPaymentMethodUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/accounts/{p_id}/stripe_set_default_payment_method/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_method_set_default.AccountStripePaymentMethodSetDefault,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_payment_method_set_default.AccountStripePaymentMethodSetDefault,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_stripe_setup_intents_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_stripe_setup_intents_retrieve.param_model.AccountsStripeSetupIntentsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_stripe_setup_intents_get.AccountStripeSetupIntentsGet:
        import gsmtasks.paths.accounts_stripe_setup_intents_retrieve.param_model

        param_model = gsmtasks.paths.accounts_stripe_setup_intents_retrieve.param_model.AccountsStripeSetupIntentsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/accounts/{p_id}/stripe_setup_intents/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_intents_get.AccountStripeSetupIntentsGet,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_stripe_setup_intents_get.AccountStripeSetupIntentsGet,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_update(
        self,
        request_body: gsmtasks.components.schemas.account.Account,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_update.param_model.AccountsUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account.Account:
        import gsmtasks.paths.accounts_update.param_model

        param_model = gsmtasks.paths.accounts_update.param_model.AccountsUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/accounts/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account.Account,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account.Account,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_workers_create(
        self,
        request_body: gsmtasks.components.schemas.account_user.AccountUser,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_workers_create.param_model.AccountsWorkersCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_user.AccountUser:
        import gsmtasks.paths.accounts_workers_create.param_model

        param_model = (
            gsmtasks.paths.accounts_workers_create.param_model.AccountsWorkersCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/accounts/{p_id}/workers/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_user.AccountUser,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_user.AccountUser,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def accounts_workers_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_workers_destroy.param_model.AccountsWorkersDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.accounts_workers_destroy.param_model

        param_model = (
            gsmtasks.paths.accounts_workers_destroy.param_model.AccountsWorkersDestroy(
                **locals()
            )
        )
        return await super()._request(
            "DELETE",
            f"/accounts/{p_id}/workers/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def accounts_workers_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.accounts_workers_retrieve.param_model.AccountsWorkersRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.account_user.AccountUser:
        import gsmtasks.paths.accounts_workers_retrieve.param_model

        param_model = gsmtasks.paths.accounts_workers_retrieve.param_model.AccountsWorkersRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/accounts/{p_id}/workers/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.account_user.AccountUser,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.account_user.AccountUser,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def addons_list(
        self,
        *,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.addons_list.param_model.AddonsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.addon.Addon,]:
        import gsmtasks.paths.addons_list.param_model

        param_model = gsmtasks.paths.addons_list.param_model.AddonsList(**locals())
        return await super()._request(
            "GET",
            f"/addons/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.addon.Addon
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.addon.Addon
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def addons_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.addons_retrieve.param_model.AddonsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.addon.Addon:
        import gsmtasks.paths.addons_retrieve.param_model

        param_model = gsmtasks.paths.addons_retrieve.param_model.AddonsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/addons/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.addon.Addon,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.addon.Addon,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def authenticate_create(
        self,
        request_body: gsmtasks.components.schemas.auth_token.AuthToken,
        /,
    ) -> gsmtasks.components.schemas.auth_token.AuthToken:
        param_model = None
        return await super()._request(
            "POST",
            f"/authenticate/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json": gsmtasks.components.schemas.auth_token.AuthToken,
                },
            },
        )

    async def billing_customers_client_token_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_customers_client_token_retrieve.param_model.BillingCustomersClientTokenRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.braintree_customer.BraintreeCustomer:
        import gsmtasks.paths.billing_customers_client_token_retrieve.param_model

        param_model = gsmtasks.paths.billing_customers_client_token_retrieve.param_model.BillingCustomersClientTokenRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/billing/customers/{p_id}/client_token/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_customers_create(
        self,
        request_body: gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.billing_customers_create.param_model.BillingCustomersCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.braintree_customer.BraintreeCustomer:
        import gsmtasks.paths.billing_customers_create.param_model

        param_model = (
            gsmtasks.paths.billing_customers_create.param_model.BillingCustomersCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/billing/customers/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_customers_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.billing_customers_list.param_model.BillingCustomersListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,]:
        import gsmtasks.paths.billing_customers_list.param_model

        param_model = (
            gsmtasks.paths.billing_customers_list.param_model.BillingCustomersList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/billing/customers/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.braintree_customer.BraintreeCustomer
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.braintree_customer.BraintreeCustomer
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_customers_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_braintree_customer.PatchedBraintreeCustomer,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_customers_partial_update.param_model.BillingCustomersPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.braintree_customer.BraintreeCustomer:
        import gsmtasks.paths.billing_customers_partial_update.param_model

        param_model = gsmtasks.paths.billing_customers_partial_update.param_model.BillingCustomersPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/billing/customers/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_customers_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_customers_retrieve.param_model.BillingCustomersRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.braintree_customer.BraintreeCustomer:
        import gsmtasks.paths.billing_customers_retrieve.param_model

        param_model = gsmtasks.paths.billing_customers_retrieve.param_model.BillingCustomersRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/billing/customers/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_customers_update(
        self,
        request_body: gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_customers_update.param_model.BillingCustomersUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.braintree_customer.BraintreeCustomer:
        import gsmtasks.paths.billing_customers_update.param_model

        param_model = (
            gsmtasks.paths.billing_customers_update.param_model.BillingCustomersUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PUT",
            f"/billing/customers/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.braintree_customer.BraintreeCustomer,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_invoices_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_billing_method: typing.Union[
            gsmtasks.paths.billing_invoices_list.param_model.BillingInvoicesListBillingMethod,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_confirmed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.billing_invoices_list.param_model.BillingInvoicesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.billing_invoices_list.param_model.BillingInvoicesListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.invoice.Invoice,]:
        import gsmtasks.paths.billing_invoices_list.param_model

        param_model = (
            gsmtasks.paths.billing_invoices_list.param_model.BillingInvoicesList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/billing/invoices/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.invoice.Invoice
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.invoice.Invoice
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_invoices_mark_as_paid_create(
        self,
        request_body: gsmtasks.components.schemas.invoice.Invoice,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_invoices_mark_as_paid_create.param_model.BillingInvoicesMarkAsPaidCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.invoice.Invoice:
        import gsmtasks.paths.billing_invoices_mark_as_paid_create.param_model

        param_model = gsmtasks.paths.billing_invoices_mark_as_paid_create.param_model.BillingInvoicesMarkAsPaidCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/billing/invoices/{p_id}/mark_as_paid/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.invoice.Invoice,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.invoice.Invoice,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_invoices_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_invoice.PatchedInvoice,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_invoices_partial_update.param_model.BillingInvoicesPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.invoice.Invoice:
        import gsmtasks.paths.billing_invoices_partial_update.param_model

        param_model = gsmtasks.paths.billing_invoices_partial_update.param_model.BillingInvoicesPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/billing/invoices/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.invoice.Invoice,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.invoice.Invoice,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_invoices_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_invoices_retrieve.param_model.BillingInvoicesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.invoice.Invoice:
        import gsmtasks.paths.billing_invoices_retrieve.param_model

        param_model = gsmtasks.paths.billing_invoices_retrieve.param_model.BillingInvoicesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/billing/invoices/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.invoice.Invoice,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.invoice.Invoice,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_invoices_update(
        self,
        request_body: gsmtasks.components.schemas.invoice.Invoice,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_invoices_update.param_model.BillingInvoicesUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.invoice.Invoice:
        import gsmtasks.paths.billing_invoices_update.param_model

        param_model = (
            gsmtasks.paths.billing_invoices_update.param_model.BillingInvoicesUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PUT",
            f"/billing/invoices/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.invoice.Invoice,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.invoice.Invoice,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_stripe_payments_list(
        self,
        *,
        q_billable_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.billing_stripe_payments_list.param_model.BillingStripePaymentsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_invoice: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.billing_stripe_payments_list.param_model.BillingStripePaymentsListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_stripe_state: typing.Union[
            gsmtasks.paths.billing_stripe_payments_list.param_model.BillingStripePaymentsListStripeState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.stripe_payment.StripePayment,]:
        import gsmtasks.paths.billing_stripe_payments_list.param_model

        param_model = gsmtasks.paths.billing_stripe_payments_list.param_model.BillingStripePaymentsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/billing/stripe_payments/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.stripe_payment.StripePayment
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.stripe_payment.StripePayment
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_stripe_payments_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_stripe_payments_retrieve.param_model.BillingStripePaymentsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.stripe_payment.StripePayment:
        import gsmtasks.paths.billing_stripe_payments_retrieve.param_model

        param_model = gsmtasks.paths.billing_stripe_payments_retrieve.param_model.BillingStripePaymentsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/billing/stripe_payments/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.stripe_payment.StripePayment,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.stripe_payment.StripePayment,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_transactions_list(
        self,
        *,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_customer: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.billing_transactions_list.param_model.BillingTransactionsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_invoice__account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.billing_transactions_list.param_model.BillingTransactionsListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.braintree_transaction.BraintreeTransaction,]:
        import gsmtasks.paths.billing_transactions_list.param_model

        param_model = gsmtasks.paths.billing_transactions_list.param_model.BillingTransactionsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/billing/transactions/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.braintree_transaction.BraintreeTransaction
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.braintree_transaction.BraintreeTransaction
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def billing_transactions_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.billing_transactions_retrieve.param_model.BillingTransactionsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.braintree_transaction.BraintreeTransaction:
        import gsmtasks.paths.billing_transactions_retrieve.param_model

        param_model = gsmtasks.paths.billing_transactions_retrieve.param_model.BillingTransactionsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/billing/transactions/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.braintree_transaction.BraintreeTransaction,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.braintree_transaction.BraintreeTransaction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def client_roles_create(
        self,
        request_body: gsmtasks.components.schemas.client_role.ClientRole,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.client_roles_create.param_model.ClientRolesCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.client_role.ClientRole:
        import gsmtasks.paths.client_roles_create.param_model

        param_model = gsmtasks.paths.client_roles_create.param_model.ClientRolesCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/client_roles/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def client_roles_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_client: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.client_roles_list.param_model.ClientRolesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_active: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_manager: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.client_role.ClientRole,]:
        import gsmtasks.paths.client_roles_list.param_model

        param_model = gsmtasks.paths.client_roles_list.param_model.ClientRolesList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/client_roles/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.client_role.ClientRole
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.client_role.ClientRole
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def client_roles_notify_create(
        self,
        request_body: gsmtasks.components.schemas.client_role.ClientRole,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.client_roles_notify_create.param_model.ClientRolesNotifyCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.client_role.ClientRole:
        import gsmtasks.paths.client_roles_notify_create.param_model

        param_model = gsmtasks.paths.client_roles_notify_create.param_model.ClientRolesNotifyCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/client_roles/{p_id}/notify/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def client_roles_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_client_role.PatchedClientRole,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.client_roles_partial_update.param_model.ClientRolesPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.client_role.ClientRole:
        import gsmtasks.paths.client_roles_partial_update.param_model

        param_model = gsmtasks.paths.client_roles_partial_update.param_model.ClientRolesPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/client_roles/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def client_roles_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.client_roles_retrieve.param_model.ClientRolesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.client_role.ClientRole:
        import gsmtasks.paths.client_roles_retrieve.param_model

        param_model = (
            gsmtasks.paths.client_roles_retrieve.param_model.ClientRolesRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/client_roles/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def client_roles_update(
        self,
        request_body: gsmtasks.components.schemas.client_role.ClientRole,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.client_roles_update.param_model.ClientRolesUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.client_role.ClientRole:
        import gsmtasks.paths.client_roles_update.param_model

        param_model = gsmtasks.paths.client_roles_update.param_model.ClientRolesUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/client_roles/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.client_role.ClientRole,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def clients_create(
        self,
        request_body: gsmtasks.components.schemas.client.Client,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.clients_create.param_model.ClientsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.client.Client:
        import gsmtasks.paths.clients_create.param_model

        param_model = gsmtasks.paths.clients_create.param_model.ClientsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/clients/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.client.Client,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.client.Client,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def clients_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.clients_list.param_model.ClientsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_slug: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.client.Client,]:
        import gsmtasks.paths.clients_list.param_model

        param_model = gsmtasks.paths.clients_list.param_model.ClientsList(**locals())
        return await super()._request(
            "GET",
            f"/clients/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.client.Client
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.client.Client
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def clients_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_client.PatchedClient,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.clients_partial_update.param_model.ClientsPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.client.Client:
        import gsmtasks.paths.clients_partial_update.param_model

        param_model = (
            gsmtasks.paths.clients_partial_update.param_model.ClientsPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/clients/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.client.Client,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.client.Client,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def clients_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.clients_retrieve.param_model.ClientsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.client.Client:
        import gsmtasks.paths.clients_retrieve.param_model

        param_model = gsmtasks.paths.clients_retrieve.param_model.ClientsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/clients/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.client.Client,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.client.Client,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def clients_update(
        self,
        request_body: gsmtasks.components.schemas.client.Client,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.clients_update.param_model.ClientsUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.client.Client:
        import gsmtasks.paths.clients_update.param_model

        param_model = gsmtasks.paths.clients_update.param_model.ClientsUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/clients/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.client.Client,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.client.Client,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def configurations_list(
        self,
        *,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.configurations_list.param_model.ConfigurationsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[
        gsmtasks.components.schemas.configuration_serializer_v2.ConfigurationSerializerV2,
    ]:
        import gsmtasks.paths.configurations_list.param_model

        param_model = gsmtasks.paths.configurations_list.param_model.ConfigurationsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/configurations/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.configuration_serializer_v2.ConfigurationSerializerV2
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.configuration_serializer_v2.ConfigurationSerializerV2
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def contact_address_exports_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_fields: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.contact_address_exports_list.param_model.ContactAddressExportsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_orderer: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_receiver: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sourcecontact__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sourcecontact__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sourcecontact__name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sourcecontact__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sourcecontact__name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.contact_address_export.ContactAddressExport,]:
        import gsmtasks.paths.contact_address_exports_list.param_model

        param_model = gsmtasks.paths.contact_address_exports_list.param_model.ContactAddressExportsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/contact_address_exports/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.contact_address_export.ContactAddressExport
                    ],
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; version=2.4.11": list[
                        gsmtasks.components.schemas.contact_address_export.ContactAddressExport
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def contact_address_import_create(
        self,
        request_body: gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.contact_address_import_create.param_model.ContactAddressImportCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport:
        import gsmtasks.paths.contact_address_import_create.param_model

        param_model = gsmtasks.paths.contact_address_import_create.param_model.ContactAddressImportCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/contact_address_import/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def contact_address_import_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.contact_address_import_list.param_model.ContactAddressImportListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.contact_address_import_list.param_model.ContactAddressImportListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[
        gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport,
    ]:
        import gsmtasks.paths.contact_address_import_list.param_model

        param_model = gsmtasks.paths.contact_address_import_list.param_model.ContactAddressImportList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/contact_address_import/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def contact_address_import_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.contact_address_import_retrieve.param_model.ContactAddressImportRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport:
        import gsmtasks.paths.contact_address_import_retrieve.param_model

        param_model = gsmtasks.paths.contact_address_import_retrieve.param_model.ContactAddressImportRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/contact_address_import/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.contact_address_background_import.ContactAddressBackgroundImport,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def contact_addresses_create(
        self,
        request_body: gsmtasks.components.schemas.contact_address.ContactAddress,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.contact_addresses_create.param_model.ContactAddressesCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.contact_address.ContactAddress:
        import gsmtasks.paths.contact_addresses_create.param_model

        param_model = (
            gsmtasks.paths.contact_addresses_create.param_model.ContactAddressesCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/contact_addresses/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.contact_address.ContactAddress,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.contact_address.ContactAddress,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def contact_addresses_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_client: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.contact_addresses_list.param_model.ContactAddressesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_orderer: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_receiver: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.contact_address.ContactAddress,]:
        import gsmtasks.paths.contact_addresses_list.param_model

        param_model = (
            gsmtasks.paths.contact_addresses_list.param_model.ContactAddressesList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/contact_addresses/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.contact_address.ContactAddress
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.contact_address.ContactAddress
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def contact_addresses_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_contact_address.PatchedContactAddress,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.contact_addresses_partial_update.param_model.ContactAddressesPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.contact_address.ContactAddress:
        import gsmtasks.paths.contact_addresses_partial_update.param_model

        param_model = gsmtasks.paths.contact_addresses_partial_update.param_model.ContactAddressesPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/contact_addresses/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.contact_address.ContactAddress,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.contact_address.ContactAddress,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def contact_addresses_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.contact_addresses_retrieve.param_model.ContactAddressesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.contact_address.ContactAddress:
        import gsmtasks.paths.contact_addresses_retrieve.param_model

        param_model = gsmtasks.paths.contact_addresses_retrieve.param_model.ContactAddressesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/contact_addresses/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.contact_address.ContactAddress,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.contact_address.ContactAddress,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def contact_addresses_update(
        self,
        request_body: gsmtasks.components.schemas.contact_address.ContactAddress,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.contact_addresses_update.param_model.ContactAddressesUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.contact_address.ContactAddress:
        import gsmtasks.paths.contact_addresses_update.param_model

        param_model = (
            gsmtasks.paths.contact_addresses_update.param_model.ContactAddressesUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PUT",
            f"/contact_addresses/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.contact_address.ContactAddress,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.contact_address.ContactAddress,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def devices_create(
        self,
        request_body: gsmtasks.components.schemas.device.Device,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.devices_create.param_model.DevicesCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.device.Device:
        import gsmtasks.paths.devices_create.param_model

        param_model = gsmtasks.paths.devices_create.param_model.DevicesCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/devices/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.device.Device,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.device.Device,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def devices_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.devices_list.param_model.DevicesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user__account_roles__account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.device.Device,]:
        import gsmtasks.paths.devices_list.param_model

        param_model = gsmtasks.paths.devices_list.param_model.DevicesList(**locals())
        return await super()._request(
            "GET",
            f"/devices/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.device.Device
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.device.Device
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def devices_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.devices_retrieve.param_model.DevicesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.device.Device:
        import gsmtasks.paths.devices_retrieve.param_model

        param_model = gsmtasks.paths.devices_retrieve.param_model.DevicesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/devices/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.device.Device,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.device.Device,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def docs_schema_retrieve(
        self,
        *,
        q_format: typing.Union[
            gsmtasks.paths.docs_schema_retrieve.param_model.DocsSchemaRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_lang: typing.Union[
            gsmtasks.paths.docs_schema_retrieve.param_model.DocsSchemaRetrieveLang,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.paths.docs_schema_retrieve.response_body.DocsSchemaRetrieve200Response:
        import gsmtasks.paths.docs_schema_retrieve.param_model

        param_model = (
            gsmtasks.paths.docs_schema_retrieve.param_model.DocsSchemaRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/docs/schema/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.paths.docs_schema_retrieve.response_body.DocsSchemaRetrieve200,
                    "application/vnd.oai.openapi+json; version=2.4.11": gsmtasks.paths.docs_schema_retrieve.response_body.DocsSchemaRetrieve200,
                    "application/vnd.oai.openapi; version=2.4.11": gsmtasks.paths.docs_schema_retrieve.response_body.DocsSchemaRetrieve200,
                    "application/yaml; version=2.4.11": gsmtasks.paths.docs_schema_retrieve.response_body.DocsSchemaRetrieve200,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def documents_batch_delete_create(
        self,
        request_body: gsmtasks.components.schemas.document_delete_action.DocumentDeleteAction,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.documents_batch_delete_create.param_model.DocumentsBatchDeleteCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.documents_batch_delete_create.param_model

        param_model = gsmtasks.paths.documents_batch_delete_create.param_model.DocumentsBatchDeleteCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/documents/batch_delete/",
            param_model=param_model,
            request_body=request_body,
            auth=self.auth_tokenAuth,
        )

    async def documents_create(
        self,
        request_body: typing.Union[
            list[
                gsmtasks.components.schemas.document.Document,
            ],
            gsmtasks.components.schemas.document.Document,
        ],
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.documents_create.param_model.DocumentsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.document.Document,
        list[
            gsmtasks.components.schemas.document.Document,
        ],
    ]:
        import gsmtasks.paths.documents_create.param_model

        param_model = gsmtasks.paths.documents_create.param_model.DocumentsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/documents/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": typing.Union[
                        list[gsmtasks.components.schemas.document.Document],
                        gsmtasks.components.schemas.document.Document,
                    ],
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.document.Document,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def documents_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.documents_destroy.param_model.DocumentsDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.documents_destroy.param_model

        param_model = gsmtasks.paths.documents_destroy.param_model.DocumentsDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/documents/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def documents_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.documents_list.param_model.DocumentsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_mimetype: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source: typing.Union[
            gsmtasks.paths.documents_list.param_model.DocumentsListSource,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.document.Document,]:
        import gsmtasks.paths.documents_list.param_model

        param_model = gsmtasks.paths.documents_list.param_model.DocumentsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/documents/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.document.Document
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.document.Document
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def documents_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.documents_retrieve.param_model.DocumentsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.document.Document:
        import gsmtasks.paths.documents_retrieve.param_model

        param_model = gsmtasks.paths.documents_retrieve.param_model.DocumentsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/documents/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.document.Document,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.document.Document,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def emails_create(
        self,
        request_body: gsmtasks.components.schemas.email.Email,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.emails_create.param_model.EmailsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.email.Email:
        import gsmtasks.paths.emails_create.param_model

        param_model = gsmtasks.paths.emails_create.param_model.EmailsCreate(**locals())
        return await super()._request(
            "POST",
            f"/emails/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.email.Email,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.email.Email,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def emails_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.emails_destroy.param_model.EmailsDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.emails_destroy.param_model

        param_model = gsmtasks.paths.emails_destroy.param_model.EmailsDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/emails/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def emails_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.emails_list.param_model.EmailsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_from_email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_from_email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_message: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_message__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reply_to_email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reply_to_email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.emails_list.param_model.EmailsListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_subject: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_subject__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.email.Email,]:
        import gsmtasks.paths.emails_list.param_model

        param_model = gsmtasks.paths.emails_list.param_model.EmailsList(**locals())
        return await super()._request(
            "GET",
            f"/emails/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.email.Email
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.email.Email
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def emails_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_email.PatchedEmail,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.emails_partial_update.param_model.EmailsPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.email.Email:
        import gsmtasks.paths.emails_partial_update.param_model

        param_model = (
            gsmtasks.paths.emails_partial_update.param_model.EmailsPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/emails/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.email.Email,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.email.Email,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def emails_resend_create(
        self,
        request_body: gsmtasks.components.schemas.email.Email,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.emails_resend_create.param_model.EmailsResendCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.email.Email:
        import gsmtasks.paths.emails_resend_create.param_model

        param_model = (
            gsmtasks.paths.emails_resend_create.param_model.EmailsResendCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/emails/{p_id}/resend/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.email.Email,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.email.Email,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def emails_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.emails_retrieve.param_model.EmailsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.email.Email:
        import gsmtasks.paths.emails_retrieve.param_model

        param_model = gsmtasks.paths.emails_retrieve.param_model.EmailsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/emails/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.email.Email,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.email.Email,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def emails_update(
        self,
        request_body: gsmtasks.components.schemas.email.Email,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.emails_update.param_model.EmailsUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.email.Email:
        import gsmtasks.paths.emails_update.param_model

        param_model = gsmtasks.paths.emails_update.param_model.EmailsUpdate(**locals())
        return await super()._request(
            "PUT",
            f"/emails/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.email.Email,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.email.Email,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def exports_create(
        self,
        request_body: gsmtasks.components.schemas.export.Export,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.exports_create.param_model.ExportsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.export.Export:
        import gsmtasks.paths.exports_create.param_model

        param_model = gsmtasks.paths.exports_create.param_model.ExportsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/exports/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.export.Export,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.export.Export,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def exports_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.exports_destroy.param_model.ExportsDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.exports_destroy.param_model

        param_model = gsmtasks.paths.exports_destroy.param_model.ExportsDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/exports/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def exports_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.exports_list.param_model.ExportsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.export.Export,]:
        import gsmtasks.paths.exports_list.param_model

        param_model = gsmtasks.paths.exports_list.param_model.ExportsList(**locals())
        return await super()._request(
            "GET",
            f"/exports/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.export.Export
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.export.Export
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def exports_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_export.PatchedExport,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.exports_partial_update.param_model.ExportsPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.export.Export:
        import gsmtasks.paths.exports_partial_update.param_model

        param_model = (
            gsmtasks.paths.exports_partial_update.param_model.ExportsPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/exports/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.export.Export,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.export.Export,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def exports_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.exports_retrieve.param_model.ExportsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.export.Export:
        import gsmtasks.paths.exports_retrieve.param_model

        param_model = gsmtasks.paths.exports_retrieve.param_model.ExportsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/exports/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.export.Export,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.export.Export,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def exports_update(
        self,
        request_body: gsmtasks.components.schemas.export.Export,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.exports_update.param_model.ExportsUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.export.Export:
        import gsmtasks.paths.exports_update.param_model

        param_model = gsmtasks.paths.exports_update.param_model.ExportsUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/exports/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.export.Export,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.export.Export,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def file_uploads_create(
        self,
        request_body: typing.Union[
            list[
                gsmtasks.components.schemas.s3_file_upload.S3FileUpload,
            ],
            gsmtasks.components.schemas.s3_file_upload.S3FileUpload,
        ],
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.file_uploads_create.param_model.FileUploadsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.s3_file_upload.S3FileUpload,
        list[
            gsmtasks.components.schemas.s3_file_upload.S3FileUpload,
        ],
    ]:
        import gsmtasks.paths.file_uploads_create.param_model

        param_model = gsmtasks.paths.file_uploads_create.param_model.FileUploadsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/file_uploads/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": typing.Union[
                        list[gsmtasks.components.schemas.s3_file_upload.S3FileUpload],
                        gsmtasks.components.schemas.s3_file_upload.S3FileUpload,
                    ],
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.s3_file_upload.S3FileUpload,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def file_uploads_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.file_uploads_list.param_model.FileUploadsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source: typing.Union[
            gsmtasks.paths.file_uploads_list.param_model.FileUploadsListSource,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.s3_file_upload.S3FileUpload,]:
        import gsmtasks.paths.file_uploads_list.param_model

        param_model = gsmtasks.paths.file_uploads_list.param_model.FileUploadsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/file_uploads/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.s3_file_upload.S3FileUpload
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.s3_file_upload.S3FileUpload
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def file_uploads_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.file_uploads_retrieve.param_model.FileUploadsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.s3_file_upload.S3FileUpload:
        import gsmtasks.paths.file_uploads_retrieve.param_model

        param_model = (
            gsmtasks.paths.file_uploads_retrieve.param_model.FileUploadsRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/file_uploads/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.s3_file_upload.S3FileUpload,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.s3_file_upload.S3FileUpload,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def formrules_create(
        self,
        request_body: gsmtasks.components.schemas.form_rule.FormRule,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.formrules_create.param_model.FormrulesCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.form_rule.FormRule:
        import gsmtasks.paths.formrules_create.param_model

        param_model = gsmtasks.paths.formrules_create.param_model.FormrulesCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/formrules/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.form_rule.FormRule,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.form_rule.FormRule,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def formrules_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.formrules_destroy.param_model.FormrulesDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.formrules_destroy.param_model

        param_model = gsmtasks.paths.formrules_destroy.param_model.FormrulesDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/formrules/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def formrules_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.formrules_list.param_model.FormrulesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.form_rule.FormRule,]:
        import gsmtasks.paths.formrules_list.param_model

        param_model = gsmtasks.paths.formrules_list.param_model.FormrulesList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/formrules/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.form_rule.FormRule
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.form_rule.FormRule
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def formrules_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_form_rule.PatchedFormRule,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.formrules_partial_update.param_model.FormrulesPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.form_rule.FormRule:
        import gsmtasks.paths.formrules_partial_update.param_model

        param_model = (
            gsmtasks.paths.formrules_partial_update.param_model.FormrulesPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/formrules/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.form_rule.FormRule,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.form_rule.FormRule,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def formrules_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.formrules_retrieve.param_model.FormrulesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.form_rule.FormRule:
        import gsmtasks.paths.formrules_retrieve.param_model

        param_model = gsmtasks.paths.formrules_retrieve.param_model.FormrulesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/formrules/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.form_rule.FormRule,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.form_rule.FormRule,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def formrules_update(
        self,
        request_body: gsmtasks.components.schemas.form_rule.FormRule,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.formrules_update.param_model.FormrulesUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.form_rule.FormRule:
        import gsmtasks.paths.formrules_update.param_model

        param_model = gsmtasks.paths.formrules_update.param_model.FormrulesUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/formrules/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.form_rule.FormRule,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.form_rule.FormRule,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def integrations_create(
        self,
        request_body: gsmtasks.components.schemas.integration_request.IntegrationRequest,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.integrations_create.param_model.IntegrationsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.integration_request.IntegrationRequest:
        import gsmtasks.paths.integrations_create.param_model

        param_model = gsmtasks.paths.integrations_create.param_model.IntegrationsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/integrations/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.integration_request.IntegrationRequest,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.integration_request.IntegrationRequest,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def metafields_create(
        self,
        request_body: gsmtasks.components.schemas.metafield.Metafield,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.metafields_create.param_model.MetafieldsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.metafield.Metafield:
        import gsmtasks.paths.metafields_create.param_model

        param_model = gsmtasks.paths.metafields_create.param_model.MetafieldsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/metafields/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.metafield.Metafield,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.metafield.Metafield,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def metafields_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.metafields_destroy.param_model.MetafieldsDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.metafields_destroy.param_model

        param_model = gsmtasks.paths.metafields_destroy.param_model.MetafieldsDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/metafields/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def metafields_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.metafields_list.param_model.MetafieldsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_editable: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_editable_assignee: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_persistent: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_required: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_searchable: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_key: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_label: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_namespace: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_show_in_detail_view: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_show_in_list_view: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_show_in_mobile_app: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_show_in_pod: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_show_when_task_type_assignment: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_show_when_task_type_drop_off: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_show_when_task_type_pick_up: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_value_type: typing.Union[
            gsmtasks.paths.metafields_list.param_model.MetafieldsListValueType,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.metafield.Metafield,]:
        import gsmtasks.paths.metafields_list.param_model

        param_model = gsmtasks.paths.metafields_list.param_model.MetafieldsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/metafields/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.metafield.Metafield
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.metafield.Metafield
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def metafields_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_metafield.PatchedMetafield,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.metafields_partial_update.param_model.MetafieldsPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.metafield.Metafield:
        import gsmtasks.paths.metafields_partial_update.param_model

        param_model = gsmtasks.paths.metafields_partial_update.param_model.MetafieldsPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/metafields/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.metafield.Metafield,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.metafield.Metafield,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def metafields_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.metafields_retrieve.param_model.MetafieldsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.metafield.Metafield:
        import gsmtasks.paths.metafields_retrieve.param_model

        param_model = gsmtasks.paths.metafields_retrieve.param_model.MetafieldsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/metafields/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.metafield.Metafield,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.metafield.Metafield,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def metafields_update(
        self,
        request_body: gsmtasks.components.schemas.metafield.Metafield,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.metafields_update.param_model.MetafieldsUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.metafield.Metafield:
        import gsmtasks.paths.metafields_update.param_model

        param_model = gsmtasks.paths.metafields_update.param_model.MetafieldsUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/metafields/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.metafield.Metafield,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.metafield.Metafield,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def notification_templates_create(
        self,
        request_body: gsmtasks.components.schemas.notification_template.NotificationTemplate,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.notification_templates_create.param_model.NotificationTemplatesCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.notification_template.NotificationTemplate:
        import gsmtasks.paths.notification_templates_create.param_model

        param_model = gsmtasks.paths.notification_templates_create.param_model.NotificationTemplatesCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/notification_templates/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.notification_template.NotificationTemplate,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.notification_template.NotificationTemplate,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def notification_templates_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.notification_templates_destroy.param_model.NotificationTemplatesDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.notification_templates_destroy.param_model

        param_model = gsmtasks.paths.notification_templates_destroy.param_model.NotificationTemplatesDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/notification_templates/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def notification_templates_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_event: typing.Union[
            gsmtasks.paths.notification_templates_list.param_model.NotificationTemplatesListEvent,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.notification_templates_list.param_model.NotificationTemplatesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_active: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_recipient: typing.Union[
            gsmtasks.paths.notification_templates_list.param_model.NotificationTemplatesListRecipient,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_via_app: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_via_email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_via_sms: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.notification_template.NotificationTemplate,]:
        import gsmtasks.paths.notification_templates_list.param_model

        param_model = gsmtasks.paths.notification_templates_list.param_model.NotificationTemplatesList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/notification_templates/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.notification_template.NotificationTemplate
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.notification_template.NotificationTemplate
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def notification_templates_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_notification_template.PatchedNotificationTemplate,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.notification_templates_partial_update.param_model.NotificationTemplatesPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.notification_template.NotificationTemplate:
        import gsmtasks.paths.notification_templates_partial_update.param_model

        param_model = gsmtasks.paths.notification_templates_partial_update.param_model.NotificationTemplatesPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/notification_templates/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.notification_template.NotificationTemplate,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.notification_template.NotificationTemplate,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def notification_templates_render_create(
        self,
        request_body: gsmtasks.components.schemas.render_request.RenderRequest,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.notification_templates_render_create.param_model.NotificationTemplatesRenderCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.render_request.RenderRequest:
        import gsmtasks.paths.notification_templates_render_create.param_model

        param_model = gsmtasks.paths.notification_templates_render_create.param_model.NotificationTemplatesRenderCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/notification_templates/{p_id}/render/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.render_request.RenderRequest,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.render_request.RenderRequest,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def notification_templates_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.notification_templates_retrieve.param_model.NotificationTemplatesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.notification_template.NotificationTemplate:
        import gsmtasks.paths.notification_templates_retrieve.param_model

        param_model = gsmtasks.paths.notification_templates_retrieve.param_model.NotificationTemplatesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/notification_templates/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.notification_template.NotificationTemplate,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.notification_template.NotificationTemplate,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def notification_templates_update(
        self,
        request_body: gsmtasks.components.schemas.notification_template.NotificationTemplate,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.notification_templates_update.param_model.NotificationTemplatesUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.notification_template.NotificationTemplate:
        import gsmtasks.paths.notification_templates_update.param_model

        param_model = gsmtasks.paths.notification_templates_update.param_model.NotificationTemplatesUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/notification_templates/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.notification_template.NotificationTemplate,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.notification_template.NotificationTemplate,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def notifications_create(
        self,
        request_body: gsmtasks.components.schemas.notification.Notification,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.notifications_create.param_model.NotificationsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.notification.Notification:
        import gsmtasks.paths.notifications_create.param_model

        param_model = (
            gsmtasks.paths.notifications_create.param_model.NotificationsCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/notifications/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.notification.Notification,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.notification.Notification,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def notifications_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_event: typing.Union[
            gsmtasks.paths.notifications_list.param_model.NotificationsListEvent,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.notifications_list.param_model.NotificationsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_recipient: typing.Union[
            gsmtasks.paths.notifications_list.param_model.NotificationsListRecipient,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_via_app: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_via_email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_via_sms: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.notification.Notification,]:
        import gsmtasks.paths.notifications_list.param_model

        param_model = gsmtasks.paths.notifications_list.param_model.NotificationsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/notifications/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.notification.Notification
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.notification.Notification
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def notifications_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.notifications_retrieve.param_model.NotificationsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.notification.Notification:
        import gsmtasks.paths.notifications_retrieve.param_model

        param_model = (
            gsmtasks.paths.notifications_retrieve.param_model.NotificationsRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/notifications/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.notification.Notification,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.notification.Notification,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def orders_create(
        self,
        request_body: gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2,
        /,
    ) -> gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2:
        param_model = None
        return await super()._request(
            "POST",
            f"/orders/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def orders_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2,]:
        import gsmtasks.paths.orders_list.param_model

        param_model = gsmtasks.paths.orders_list.param_model.OrdersList(**locals())
        return await super()._request(
            "GET",
            f"/orders/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def orders_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_order_serializer_v2.PatchedOrderSerializerV2,
        /,
        *,
        p_id: uuid.UUID,
    ) -> gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2:
        import gsmtasks.paths.orders_partial_update.param_model

        param_model = (
            gsmtasks.paths.orders_partial_update.param_model.OrdersPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/orders/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def orders_retrieve(
        self,
        *,
        p_id: uuid.UUID,
    ) -> gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2:
        import gsmtasks.paths.orders_retrieve.param_model

        param_model = gsmtasks.paths.orders_retrieve.param_model.OrdersRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/orders/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def orders_update(
        self,
        request_body: gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2,
        /,
        *,
        p_id: uuid.UUID,
    ) -> gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2:
        import gsmtasks.paths.orders_update.param_model

        param_model = gsmtasks.paths.orders_update.param_model.OrdersUpdate(**locals())
        return await super()._request(
            "PUT",
            f"/orders/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.order_serializer_v2.OrderSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def password_change_create(
        self,
        request_body: gsmtasks.components.schemas.password_change.PasswordChange,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.password_change_create.param_model.PasswordChangeCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.password_change.PasswordChange:
        import gsmtasks.paths.password_change_create.param_model

        param_model = (
            gsmtasks.paths.password_change_create.param_model.PasswordChangeCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/password_change/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.password_change.PasswordChange,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.password_change.PasswordChange,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def password_reset_confirm_create(
        self,
        request_body: gsmtasks.components.schemas.password_reset_confirm.PasswordResetConfirm,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.password_reset_confirm_create.param_model.PasswordResetConfirmCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.password_reset_confirm.PasswordResetConfirm:
        import gsmtasks.paths.password_reset_confirm_create.param_model

        param_model = gsmtasks.paths.password_reset_confirm_create.param_model.PasswordResetConfirmCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/password_reset_confirm/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.password_reset_confirm.PasswordResetConfirm,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.password_reset_confirm.PasswordResetConfirm,
                },
            },
        )

    async def password_reset_create(
        self,
        request_body: gsmtasks.components.schemas.password_reset.PasswordReset,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.password_reset_create.param_model.PasswordResetCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.password_reset.PasswordReset:
        import gsmtasks.paths.password_reset_create.param_model

        param_model = (
            gsmtasks.paths.password_reset_create.param_model.PasswordResetCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/password_reset/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.password_reset.PasswordReset,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.password_reset.PasswordReset,
                },
            },
        )

    async def push_notifications_create(
        self,
        request_body: gsmtasks.components.schemas.push_notification.PushNotification,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.push_notifications_create.param_model.PushNotificationsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.push_notification.PushNotification:
        import gsmtasks.paths.push_notifications_create.param_model

        param_model = gsmtasks.paths.push_notifications_create.param_model.PushNotificationsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/push_notifications/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def push_notifications_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.push_notifications_destroy.param_model.PushNotificationsDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.push_notifications_destroy.param_model

        param_model = gsmtasks.paths.push_notifications_destroy.param_model.PushNotificationsDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/push_notifications/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def push_notifications_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_event: typing.Union[
            gsmtasks.paths.push_notifications_list.param_model.PushNotificationsListEvent,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_event__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.push_notifications_list.param_model.PushNotificationsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_message: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_message__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_pending_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.push_notifications_list.param_model.PushNotificationsListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_subject: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_subject__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.push_notification.PushNotification,]:
        import gsmtasks.paths.push_notifications_list.param_model

        param_model = (
            gsmtasks.paths.push_notifications_list.param_model.PushNotificationsList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/push_notifications/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.push_notification.PushNotification
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.push_notification.PushNotification
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def push_notifications_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_push_notification.PatchedPushNotification,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.push_notifications_partial_update.param_model.PushNotificationsPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.push_notification.PushNotification:
        import gsmtasks.paths.push_notifications_partial_update.param_model

        param_model = gsmtasks.paths.push_notifications_partial_update.param_model.PushNotificationsPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/push_notifications/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def push_notifications_resend_create(
        self,
        request_body: gsmtasks.components.schemas.push_notification.PushNotification,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.push_notifications_resend_create.param_model.PushNotificationsResendCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.push_notification.PushNotification:
        import gsmtasks.paths.push_notifications_resend_create.param_model

        param_model = gsmtasks.paths.push_notifications_resend_create.param_model.PushNotificationsResendCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/push_notifications/{p_id}/resend/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def push_notifications_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.push_notifications_retrieve.param_model.PushNotificationsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.push_notification.PushNotification:
        import gsmtasks.paths.push_notifications_retrieve.param_model

        param_model = gsmtasks.paths.push_notifications_retrieve.param_model.PushNotificationsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/push_notifications/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def push_notifications_update(
        self,
        request_body: gsmtasks.components.schemas.push_notification.PushNotification,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.push_notifications_update.param_model.PushNotificationsUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.push_notification.PushNotification:
        import gsmtasks.paths.push_notifications_update.param_model

        param_model = gsmtasks.paths.push_notifications_update.param_model.PushNotificationsUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/push_notifications/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.push_notification.PushNotification,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def recurrences_create(
        self,
        request_body: gsmtasks.components.schemas.recurrence.Recurrence,
        /,
    ) -> gsmtasks.components.schemas.recurrence.Recurrence:
        param_model = None
        return await super()._request(
            "POST",
            f"/recurrences/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.recurrence.Recurrence,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def recurrences_list(
        self,
        *,
        q_account: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_account__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assign_worker: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_active: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__address__formatted_address__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__address__formatted_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__address__formatted_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__category__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__category__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__company__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__company__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__emails__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__name__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__name__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__notes__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__phones__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__description__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__state__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.recurrence.Recurrence,]:
        import gsmtasks.paths.recurrences_list.param_model

        param_model = gsmtasks.paths.recurrences_list.param_model.RecurrencesList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/recurrences/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.recurrence.Recurrence
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def recurrences_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_recurrence.PatchedRecurrence,
        /,
        *,
        p_id: uuid.UUID,
    ) -> gsmtasks.components.schemas.recurrence.Recurrence:
        import gsmtasks.paths.recurrences_partial_update.param_model

        param_model = gsmtasks.paths.recurrences_partial_update.param_model.RecurrencesPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/recurrences/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.recurrence.Recurrence,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def recurrences_retrieve(
        self,
        *,
        p_id: uuid.UUID,
    ) -> gsmtasks.components.schemas.recurrence.Recurrence:
        import gsmtasks.paths.recurrences_retrieve.param_model

        param_model = (
            gsmtasks.paths.recurrences_retrieve.param_model.RecurrencesRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/recurrences/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.recurrence.Recurrence,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def recurrences_update(
        self,
        request_body: gsmtasks.components.schemas.recurrence.Recurrence,
        /,
        *,
        p_id: uuid.UUID,
    ) -> gsmtasks.components.schemas.recurrence.Recurrence:
        import gsmtasks.paths.recurrences_update.param_model

        param_model = gsmtasks.paths.recurrences_update.param_model.RecurrencesUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/recurrences/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.recurrence.Recurrence,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def register_create(
        self,
        request_body: gsmtasks.components.schemas.registration.Registration,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.register_create.param_model.RegisterCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.registration.Registration:
        import gsmtasks.paths.register_create.param_model

        param_model = gsmtasks.paths.register_create.param_model.RegisterCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/register/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.registration.Registration,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.registration.Registration,
                },
            },
        )

    async def reports_tasks_states_count_retrieve(
        self,
        *,
        q_account: uuid.UUID,
        q_date_from: datetime.date,
        q_date_until: datetime.date,
        q_assignee: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.reports_tasks_states_count_retrieve.param_model.ReportsTasksStatesCountRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timezone: typing.Union[
            gsmtasks.paths.reports_tasks_states_count_retrieve.param_model.ReportsTasksStatesCountRetrieveTimezone,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.tasks_states_count_response.TasksStatesCountResponse:
        import gsmtasks.paths.reports_tasks_states_count_retrieve.param_model

        param_model = gsmtasks.paths.reports_tasks_states_count_retrieve.param_model.ReportsTasksStatesCountRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/reports/tasks/states_count/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.tasks_states_count_response.TasksStatesCountResponse,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.tasks_states_count_response.TasksStatesCountResponse,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def reviews_create(
        self,
        request_body: gsmtasks.components.schemas.review.Review,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.reviews_create.param_model.ReviewsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.review.Review:
        import gsmtasks.paths.reviews_create.param_model

        param_model = gsmtasks.paths.reviews_create.param_model.ReviewsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/reviews/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.review.Review,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.review.Review,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def reviews_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.reviews_list.param_model.ReviewsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tracker: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.review.Review,]:
        import gsmtasks.paths.reviews_list.param_model

        param_model = gsmtasks.paths.reviews_list.param_model.ReviewsList(**locals())
        return await super()._request(
            "GET",
            f"/reviews/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.review.Review
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.review.Review
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def reviews_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.reviews_retrieve.param_model.ReviewsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.review.Review:
        import gsmtasks.paths.reviews_retrieve.param_model

        param_model = gsmtasks.paths.reviews_retrieve.param_model.ReviewsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/reviews/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.review.Review,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.review.Review,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def route_optimizations_commit_create(
        self,
        request_body: gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.route_optimizations_commit_create.param_model.RouteOptimizationsCommitCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2:
        import gsmtasks.paths.route_optimizations_commit_create.param_model

        param_model = gsmtasks.paths.route_optimizations_commit_create.param_model.RouteOptimizationsCommitCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/route_optimizations/{p_id}/commit/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def route_optimizations_create(
        self,
        request_body: gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.route_optimizations_create.param_model.RouteOptimizationsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2:
        import gsmtasks.paths.route_optimizations_create.param_model

        param_model = gsmtasks.paths.route_optimizations_create.param_model.RouteOptimizationsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/route_optimizations/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def route_optimizations_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignees__id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_commited_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.route_optimizations_list.param_model.RouteOptimizationsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_objective: typing.Union[
            gsmtasks.paths.route_optimizations_list.param_model.RouteOptimizationsListObjective,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_objective__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ready_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.route_optimizations_list.param_model.RouteOptimizationsListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_total_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_total_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_total_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_total_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_total_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_total_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_total_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_total_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[
        gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
    ]:
        import gsmtasks.paths.route_optimizations_list.param_model

        param_model = (
            gsmtasks.paths.route_optimizations_list.param_model.RouteOptimizationsList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/route_optimizations/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2
                    ],
                    "application/xml; version=2.4.11": list[
                        gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def route_optimizations_results_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.route_optimizations_results_retrieve.param_model.RouteOptimizationsResultsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2:
        import gsmtasks.paths.route_optimizations_results_retrieve.param_model

        param_model = gsmtasks.paths.route_optimizations_results_retrieve.param_model.RouteOptimizationsResultsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/route_optimizations/{p_id}/results/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def route_optimizations_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.route_optimizations_retrieve.param_model.RouteOptimizationsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2:
        import gsmtasks.paths.route_optimizations_retrieve.param_model

        param_model = gsmtasks.paths.route_optimizations_retrieve.param_model.RouteOptimizationsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/route_optimizations/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def route_optimizations_routes_create(
        self,
        request_body: gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.route_optimizations_routes_create.param_model.RouteOptimizationsRoutesCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2:
        import gsmtasks.paths.route_optimizations_routes_create.param_model

        param_model = gsmtasks.paths.route_optimizations_routes_create.param_model.RouteOptimizationsRoutesCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/route_optimizations/{p_id}/routes/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def route_optimizations_routes_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.route_optimizations_routes_retrieve.param_model.RouteOptimizationsRoutesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2:
        import gsmtasks.paths.route_optimizations_routes_retrieve.param_model

        param_model = gsmtasks.paths.route_optimizations_routes_retrieve.param_model.RouteOptimizationsRoutesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/route_optimizations/{p_id}/routes/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def route_optimizations_schedule_create(
        self,
        request_body: gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.route_optimizations_schedule_create.param_model.RouteOptimizationsScheduleCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2:
        import gsmtasks.paths.route_optimizations_schedule_create.param_model

        param_model = gsmtasks.paths.route_optimizations_schedule_create.param_model.RouteOptimizationsScheduleCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/route_optimizations/{p_id}/schedule/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.route_optimization_serializer_v2.RouteOptimizationSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def routes_create(
        self,
        request_body: gsmtasks.components.schemas.route.Route,
        /,
    ) -> gsmtasks.components.schemas.route.Route:
        param_model = None
        return await super()._request(
            "POST",
            f"/routes/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route.Route,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def routes_destroy(
        self,
        *,
        p_id: uuid.UUID,
    ) -> None:
        import gsmtasks.paths.routes_destroy.param_model

        param_model = gsmtasks.paths.routes_destroy.param_model.RoutesDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/routes/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def routes_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.route.Route,]:
        import gsmtasks.paths.routes_list.param_model

        param_model = gsmtasks.paths.routes_list.param_model.RoutesList(**locals())
        return await super()._request(
            "GET",
            f"/routes/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.route.Route
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def routes_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_route.PatchedRoute,
        /,
        *,
        p_id: uuid.UUID,
    ) -> gsmtasks.components.schemas.route.Route:
        import gsmtasks.paths.routes_partial_update.param_model

        param_model = (
            gsmtasks.paths.routes_partial_update.param_model.RoutesPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/routes/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route.Route,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def routes_retrieve(
        self,
        *,
        p_id: uuid.UUID,
    ) -> gsmtasks.components.schemas.route.Route:
        import gsmtasks.paths.routes_retrieve.param_model

        param_model = gsmtasks.paths.routes_retrieve.param_model.RoutesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/routes/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route.Route,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def routes_update(
        self,
        request_body: gsmtasks.components.schemas.route.Route,
        /,
        *,
        p_id: uuid.UUID,
    ) -> gsmtasks.components.schemas.route.Route:
        import gsmtasks.paths.routes_update.param_model

        param_model = gsmtasks.paths.routes_update.param_model.RoutesUpdate(**locals())
        return await super()._request(
            "PUT",
            f"/routes/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.route.Route,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def scenes_dashboard_list(
        self,
        *,
        q_account: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_account__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_data: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_proximity: typing.Union[
            gsmtasks.paths.scenes_dashboard_list.param_model.ScenesDashboardListAssigneeProximity,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_proximity__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_category: typing.Union[
            gsmtasks.paths.scenes_dashboard_list.param_model.ScenesDashboardListCategory,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_category__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_data: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.scenes_dashboard_list.param_model.ScenesDashboardListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_optimal: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_optimal__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metafields__namespace_key: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__auto_assign: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.scenes_dashboard_list.param_model.ScenesDashboardListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task_import: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task_import__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.dashboard_scene.DashboardScene,]:
        import gsmtasks.paths.scenes_dashboard_list.param_model

        param_model = (
            gsmtasks.paths.scenes_dashboard_list.param_model.ScenesDashboardList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/scenes/dashboard/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.dashboard_scene.DashboardScene
                    ],
                    "application/xml; version=2.4.11": list[
                        gsmtasks.components.schemas.dashboard_scene.DashboardScene
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def scenes_order_list_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.order_list_scene.OrderListScene,]:
        import gsmtasks.paths.scenes_order_list_list.param_model

        param_model = (
            gsmtasks.paths.scenes_order_list_list.param_model.ScenesOrderListList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/scenes/order_list/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.order_list_scene.OrderListScene
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def scenes_recurrence_list_list(
        self,
        *,
        q_account: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_account__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assign_worker: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_active: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_errored_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_recurred_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_last_scheduled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_next_scheduled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__address__formatted_address__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__address__formatted_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__address__formatted_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__category__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__category__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__company__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__company__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__emails__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__name__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__name__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__notes__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__contact__phones__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__description__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__state__exact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_tasks_data__state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.recurrence_list_scene.RecurrenceListScene,]:
        import gsmtasks.paths.scenes_recurrence_list_list.param_model

        param_model = gsmtasks.paths.scenes_recurrence_list_list.param_model.ScenesRecurrenceListList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/scenes/recurrence_list/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.recurrence_list_scene.RecurrenceListScene
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def scenes_task_list_list(
        self,
        *,
        q_account: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_account__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_data: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_proximity: typing.Union[
            gsmtasks.paths.scenes_task_list_list.param_model.ScenesTaskListListAssigneeProximity,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_proximity__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_category: typing.Union[
            gsmtasks.paths.scenes_task_list_list.param_model.ScenesTaskListListCategory,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_category__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_data: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.scenes_task_list_list.param_model.ScenesTaskListListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_optimal: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_optimal__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metafields__namespace_key: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__auto_assign: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.scenes_task_list_list.param_model.ScenesTaskListListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task_import: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task_import__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.task_list_scene.TaskListScene,]:
        import gsmtasks.paths.scenes_task_list_list.param_model

        param_model = (
            gsmtasks.paths.scenes_task_list_list.param_model.ScenesTaskListList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/scenes/task_list/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.task_list_scene.TaskListScene
                    ],
                    "application/xml; version=2.4.11": list[
                        gsmtasks.components.schemas.task_list_scene.TaskListScene
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def signatures_batch_delete_create(
        self,
        request_body: gsmtasks.components.schemas.signature_delete_action.SignatureDeleteAction,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.signatures_batch_delete_create.param_model.SignaturesBatchDeleteCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.signatures_batch_delete_create.param_model

        param_model = gsmtasks.paths.signatures_batch_delete_create.param_model.SignaturesBatchDeleteCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/signatures/batch_delete/",
            param_model=param_model,
            request_body=request_body,
            auth=self.auth_tokenAuth,
        )

    async def signatures_create(
        self,
        request_body: gsmtasks.components.schemas.signature.Signature,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.signatures_create.param_model.SignaturesCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.signature.Signature:
        import gsmtasks.paths.signatures_create.param_model

        param_model = gsmtasks.paths.signatures_create.param_model.SignaturesCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/signatures/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.signature.Signature,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.signature.Signature,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def signatures_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.signatures_destroy.param_model.SignaturesDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.signatures_destroy.param_model

        param_model = gsmtasks.paths.signatures_destroy.param_model.SignaturesDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/signatures/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def signatures_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_filename__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.signatures_list.param_model.SignaturesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_mimetype: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_source: typing.Union[
            gsmtasks.paths.signatures_list.param_model.SignaturesListSource,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.signature.Signature,]:
        import gsmtasks.paths.signatures_list.param_model

        param_model = gsmtasks.paths.signatures_list.param_model.SignaturesList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/signatures/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.signature.Signature
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.signature.Signature
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def signatures_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.signatures_retrieve.param_model.SignaturesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.signature.Signature:
        import gsmtasks.paths.signatures_retrieve.param_model

        param_model = gsmtasks.paths.signatures_retrieve.param_model.SignaturesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/signatures/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.signature.Signature,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.signature.Signature,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def sms_create(
        self,
        request_body: gsmtasks.components.schemas.sms.SMS,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.sms_create.param_model.SmsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.sms.SMS:
        import gsmtasks.paths.sms_create.param_model

        param_model = gsmtasks.paths.sms_create.param_model.SmsCreate(**locals())
        return await super()._request(
            "POST",
            f"/sms/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def sms_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.sms_destroy.param_model.SmsDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.sms_destroy.param_model

        param_model = gsmtasks.paths.sms_destroy.param_model.SmsDestroy(**locals())
        return await super()._request(
            "DELETE",
            f"/sms/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def sms_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_alphanumeric_sender_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_alphanumeric_sender_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.sms_list.param_model.SmsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_message: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_message__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_phone: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_phone__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_price: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_price__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_price__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_price__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_price__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_provider: typing.Union[
            gsmtasks.paths.sms_list.param_model.SmsListProvider,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_provider__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_received_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_segments_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_segments_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_segments_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_segments_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_segments_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sent_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.sms_list.param_model.SmsListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.sms.SMS,]:
        import gsmtasks.paths.sms_list.param_model

        param_model = gsmtasks.paths.sms_list.param_model.SmsList(**locals())
        return await super()._request(
            "GET",
            f"/sms/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.sms.SMS
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.sms.SMS
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def sms_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_sms.PatchedSMS,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.sms_partial_update.param_model.SmsPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.sms.SMS:
        import gsmtasks.paths.sms_partial_update.param_model

        param_model = gsmtasks.paths.sms_partial_update.param_model.SmsPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/sms/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def sms_resend_create(
        self,
        request_body: gsmtasks.components.schemas.sms.SMS,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.sms_resend_create.param_model.SmsResendCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.sms.SMS:
        import gsmtasks.paths.sms_resend_create.param_model

        param_model = gsmtasks.paths.sms_resend_create.param_model.SmsResendCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/sms/{p_id}/resend/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def sms_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.sms_retrieve.param_model.SmsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.sms.SMS:
        import gsmtasks.paths.sms_retrieve.param_model

        param_model = gsmtasks.paths.sms_retrieve.param_model.SmsRetrieve(**locals())
        return await super()._request(
            "GET",
            f"/sms/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def sms_update(
        self,
        request_body: gsmtasks.components.schemas.sms.SMS,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.sms_update.param_model.SmsUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.sms.SMS:
        import gsmtasks.paths.sms_update.param_model

        param_model = gsmtasks.paths.sms_update.param_model.SmsUpdate(**locals())
        return await super()._request(
            "PUT",
            f"/sms/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.sms.SMS,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_address_features_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_category: typing.Union[
            gsmtasks.paths.task_address_features_list.param_model.TaskAddressFeaturesListCategory,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.task_address_features_list.param_model.TaskAddressFeaturesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.task_address_feature.TaskAddressFeature,]:
        import gsmtasks.paths.task_address_features_list.param_model

        param_model = gsmtasks.paths.task_address_features_list.param_model.TaskAddressFeaturesList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_address_features/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.task_address_feature.TaskAddressFeature
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.task_address_feature.TaskAddressFeature
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_address_features_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_address_features_retrieve.param_model.TaskAddressFeaturesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_address_feature.TaskAddressFeature:
        import gsmtasks.paths.task_address_features_retrieve.param_model

        param_model = gsmtasks.paths.task_address_features_retrieve.param_model.TaskAddressFeaturesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_address_features/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_address_feature.TaskAddressFeature,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_address_feature.TaskAddressFeature,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_commands_create(
        self,
        request_body: gsmtasks.components.schemas.task_command.TaskCommand,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.task_commands_create.param_model.TaskCommandsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_command.TaskCommand:
        import gsmtasks.paths.task_commands_create.param_model

        param_model = (
            gsmtasks.paths.task_commands_create.param_model.TaskCommandsCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/task_commands/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_command.TaskCommand,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_command.TaskCommand,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_commands_list(
        self,
        *,
        q_accepted_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_accepted_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_accepted_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_accepted_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_accepted_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_accepted_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_accepted_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_accepted_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_accepted_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_accepted_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_action: typing.Union[
            gsmtasks.paths.task_commands_list.param_model.TaskCommandsListAction,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.task_commands_list.param_model.TaskCommandsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_rejected_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.task_commands_list.param_model.TaskCommandsListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task__account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.task_command.TaskCommand,]:
        import gsmtasks.paths.task_commands_list.param_model

        param_model = gsmtasks.paths.task_commands_list.param_model.TaskCommandsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_commands/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.task_command.TaskCommand
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.task_command.TaskCommand
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_commands_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_commands_retrieve.param_model.TaskCommandsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_command.TaskCommand:
        import gsmtasks.paths.task_commands_retrieve.param_model

        param_model = (
            gsmtasks.paths.task_commands_retrieve.param_model.TaskCommandsRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/task_commands/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_command.TaskCommand,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_command.TaskCommand,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_commands_update(
        self,
        request_body: gsmtasks.components.schemas.task_command.TaskCommand,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_commands_update.param_model.TaskCommandsUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_command.TaskCommand:
        import gsmtasks.paths.task_commands_update.param_model

        param_model = (
            gsmtasks.paths.task_commands_update.param_model.TaskCommandsUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PUT",
            f"/task_commands/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_command.TaskCommand,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_command.TaskCommand,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_event_tracks_list(
        self,
        *,
        q_assignee: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_event: typing.Union[
            gsmtasks.paths.task_event_tracks_list.param_model.TaskEventTracksListEvent,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.task_event_tracks_list.param_model.TaskEventTracksListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_from_state: typing.Union[
            gsmtasks.paths.task_event_tracks_list.param_model.TaskEventTracksListFromState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_to_state: typing.Union[
            gsmtasks.paths.task_event_tracks_list.param_model.TaskEventTracksListToState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.task_event_track.TaskEventTrack,]:
        import gsmtasks.paths.task_event_tracks_list.param_model

        param_model = (
            gsmtasks.paths.task_event_tracks_list.param_model.TaskEventTracksList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/task_event_tracks/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.task_event_track.TaskEventTrack
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.task_event_track.TaskEventTrack
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_event_tracks_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_event_tracks_retrieve.param_model.TaskEventTracksRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_event_track.TaskEventTrack:
        import gsmtasks.paths.task_event_tracks_retrieve.param_model

        param_model = gsmtasks.paths.task_event_tracks_retrieve.param_model.TaskEventTracksRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_event_tracks/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_event_track.TaskEventTrack,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_event_track.TaskEventTrack,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_events_list(
        self,
        *,
        q_assignee: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_event: typing.Union[
            gsmtasks.paths.task_events_list.param_model.TaskEventsListEvent,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_event__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_field: typing.Union[
            gsmtasks.paths.task_events_list.param_model.TaskEventsListField,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.task_events_list.param_model.TaskEventsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_from_state: typing.Union[
            gsmtasks.paths.task_events_list.param_model.TaskEventsListFromState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_from_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task__account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_to_state: typing.Union[
            gsmtasks.paths.task_events_list.param_model.TaskEventsListToState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_to_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[
        gsmtasks.components.schemas.task_event_serializer_v2.TaskEventSerializerV2,
    ]:
        import gsmtasks.paths.task_events_list.param_model

        param_model = gsmtasks.paths.task_events_list.param_model.TaskEventsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_events/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.task_event_serializer_v2.TaskEventSerializerV2
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.task_event_serializer_v2.TaskEventSerializerV2
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_events_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_events_retrieve.param_model.TaskEventsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_event_serializer_v2.TaskEventSerializerV2:
        import gsmtasks.paths.task_events_retrieve.param_model

        param_model = (
            gsmtasks.paths.task_events_retrieve.param_model.TaskEventsRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/task_events/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_event_serializer_v2.TaskEventSerializerV2,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_event_serializer_v2.TaskEventSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_exports_list(
        self,
        *,
        q_account: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_account__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_data: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_proximity: typing.Union[
            gsmtasks.paths.task_exports_list.param_model.TaskExportsListAssigneeProximity,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_proximity__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_category: typing.Union[
            gsmtasks.paths.task_exports_list.param_model.TaskExportsListCategory,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_category__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_data: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_fields: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.task_exports_list.param_model.TaskExportsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_optimal: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_optimal__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metafields__namespace_key: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__auto_assign: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.task_exports_list.param_model.TaskExportsListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task_import: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task_import__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.task_export.TaskExport,]:
        import gsmtasks.paths.task_exports_list.param_model

        param_model = gsmtasks.paths.task_exports_list.param_model.TaskExportsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_exports/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.task_export.TaskExport
                    ],
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; version=2.4.11": list[
                        gsmtasks.components.schemas.task_export.TaskExport
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_forms_create(
        self,
        request_body: gsmtasks.components.schemas.task_form.TaskForm,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.task_forms_create.param_model.TaskFormsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_form.TaskForm:
        import gsmtasks.paths.task_forms_create.param_model

        param_model = gsmtasks.paths.task_forms_create.param_model.TaskFormsCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/task_forms/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_form.TaskForm,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_form.TaskForm,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_forms_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_forms_destroy.param_model.TaskFormsDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.task_forms_destroy.param_model

        param_model = gsmtasks.paths.task_forms_destroy.param_model.TaskFormsDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/task_forms/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def task_forms_list(
        self,
        *,
        q_completed: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.task_forms_list.param_model.TaskFormsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.task_form.TaskForm,]:
        import gsmtasks.paths.task_forms_list.param_model

        param_model = gsmtasks.paths.task_forms_list.param_model.TaskFormsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_forms/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.task_form.TaskForm
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.task_form.TaskForm
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_forms_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_task_form.PatchedTaskForm,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_forms_partial_update.param_model.TaskFormsPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_form.TaskForm:
        import gsmtasks.paths.task_forms_partial_update.param_model

        param_model = (
            gsmtasks.paths.task_forms_partial_update.param_model.TaskFormsPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/task_forms/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_form.TaskForm,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_form.TaskForm,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_forms_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_forms_retrieve.param_model.TaskFormsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_form.TaskForm:
        import gsmtasks.paths.task_forms_retrieve.param_model

        param_model = gsmtasks.paths.task_forms_retrieve.param_model.TaskFormsRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_forms/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_form.TaskForm,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_form.TaskForm,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_forms_update(
        self,
        request_body: gsmtasks.components.schemas.task_form.TaskForm,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_forms_update.param_model.TaskFormsUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_form.TaskForm:
        import gsmtasks.paths.task_forms_update.param_model

        param_model = gsmtasks.paths.task_forms_update.param_model.TaskFormsUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/task_forms/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_form.TaskForm,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_form.TaskForm,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_import_create(
        self,
        request_body: gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.task_import_create.param_model.TaskImportCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport:
        import gsmtasks.paths.task_import_create.param_model

        param_model = gsmtasks.paths.task_import_create.param_model.TaskImportCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/task_import/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_import_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.task_import_list.param_model.TaskImportListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_started_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.task_import_list.param_model.TaskImportListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[
        gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport,
    ]:
        import gsmtasks.paths.task_import_list.param_model

        param_model = gsmtasks.paths.task_import_list.param_model.TaskImportList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_import/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_import_mapping_create(
        self,
        request_body: gsmtasks.components.schemas.import_mapping.ImportMapping,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.task_import_mapping_create.param_model.TaskImportMappingCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.import_mapping.ImportMapping:
        import gsmtasks.paths.task_import_mapping_create.param_model

        param_model = gsmtasks.paths.task_import_mapping_create.param_model.TaskImportMappingCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/task_import_mapping/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.import_mapping.ImportMapping,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.import_mapping.ImportMapping,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_import_mapping_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_field_names__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_field_names__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_field_names__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_field_names__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.task_import_mapping_list.param_model.TaskImportMappingListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.import_mapping.ImportMapping,]:
        import gsmtasks.paths.task_import_mapping_list.param_model

        param_model = (
            gsmtasks.paths.task_import_mapping_list.param_model.TaskImportMappingList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/task_import_mapping/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.import_mapping.ImportMapping
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.import_mapping.ImportMapping
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_import_mapping_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_import_mapping_retrieve.param_model.TaskImportMappingRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.import_mapping.ImportMapping:
        import gsmtasks.paths.task_import_mapping_retrieve.param_model

        param_model = gsmtasks.paths.task_import_mapping_retrieve.param_model.TaskImportMappingRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_import_mapping/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.import_mapping.ImportMapping,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.import_mapping.ImportMapping,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_import_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_import_retrieve.param_model.TaskImportRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport:
        import gsmtasks.paths.task_import_retrieve.param_model

        param_model = (
            gsmtasks.paths.task_import_retrieve.param_model.TaskImportRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/task_import/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.tasks_background_import.TasksBackgroundImport,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_metadatas_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.task_metadatas_list.param_model.TaskMetadatasListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.task_metadata.TaskMetadata,]:
        import gsmtasks.paths.task_metadatas_list.param_model

        param_model = gsmtasks.paths.task_metadatas_list.param_model.TaskMetadatasList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/task_metadatas/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.task_metadata.TaskMetadata
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.task_metadata.TaskMetadata
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def task_metadatas_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.task_metadatas_retrieve.param_model.TaskMetadatasRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_metadata.TaskMetadata:
        import gsmtasks.paths.task_metadatas_retrieve.param_model

        param_model = (
            gsmtasks.paths.task_metadatas_retrieve.param_model.TaskMetadatasRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/task_metadatas/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_metadata.TaskMetadata,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.task_metadata.TaskMetadata,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_accept_create(
        self,
        request_body: gsmtasks.components.schemas.task_action.TaskAction,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_accept_create.param_model.TasksAcceptCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_action.TaskAction:
        import gsmtasks.paths.tasks_accept_create.param_model

        param_model = gsmtasks.paths.tasks_accept_create.param_model.TasksAcceptCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/accept/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_account_change_create(
        self,
        request_body: gsmtasks.components.schemas.task_account_change.TaskAccountChange,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_account_change_create.param_model.TasksAccountChangeCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_account_change.TaskAccountChange:
        import gsmtasks.paths.tasks_account_change_create.param_model

        param_model = gsmtasks.paths.tasks_account_change_create.param_model.TasksAccountChangeCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/account_change/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_account_change.TaskAccountChange,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_account_change.TaskAccountChange,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_activate_create(
        self,
        request_body: gsmtasks.components.schemas.task_action.TaskAction,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_activate_create.param_model.TasksActivateCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_action.TaskAction:
        import gsmtasks.paths.tasks_activate_create.param_model

        param_model = (
            gsmtasks.paths.tasks_activate_create.param_model.TasksActivateCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/activate/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_assign_create(
        self,
        request_body: gsmtasks.components.schemas.task_assign.TaskAssign,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_assign_create.param_model.TasksAssignCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_assign.TaskAssign:
        import gsmtasks.paths.tasks_assign_create.param_model

        param_model = gsmtasks.paths.tasks_assign_create.param_model.TasksAssignCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/assign/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_assign.TaskAssign,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_assign.TaskAssign,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_cancel_create(
        self,
        request_body: gsmtasks.components.schemas.task_action.TaskAction,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_cancel_create.param_model.TasksCancelCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_action.TaskAction:
        import gsmtasks.paths.tasks_cancel_create.param_model

        param_model = gsmtasks.paths.tasks_cancel_create.param_model.TasksCancelCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/cancel/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_complete_create(
        self,
        request_body: gsmtasks.components.schemas.task_action.TaskAction,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_complete_create.param_model.TasksCompleteCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_action.TaskAction:
        import gsmtasks.paths.tasks_complete_create.param_model

        param_model = (
            gsmtasks.paths.tasks_complete_create.param_model.TasksCompleteCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/complete/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_create(
        self,
        request_body: typing.Union[
            list[
                gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
            ],
            gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
        ],
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.tasks_create.param_model.TasksCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
        list[
            gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
        ],
    ]:
        import gsmtasks.paths.tasks_create.param_model

        param_model = gsmtasks.paths.tasks_create.param_model.TasksCreate(**locals())
        return await super()._request(
            "POST",
            f"/tasks/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": typing.Union[
                        list[
                            gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2
                        ],
                        gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                    ],
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_documents_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_documents_retrieve.param_model.TasksDocumentsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2:
        import gsmtasks.paths.tasks_documents_retrieve.param_model

        param_model = (
            gsmtasks.paths.tasks_documents_retrieve.param_model.TasksDocumentsRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/tasks/{p_id}/documents/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_events_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_events_retrieve.param_model.TasksEventsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2:
        import gsmtasks.paths.tasks_events_retrieve.param_model

        param_model = (
            gsmtasks.paths.tasks_events_retrieve.param_model.TasksEventsRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/tasks/{p_id}/events/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_fail_create(
        self,
        request_body: gsmtasks.components.schemas.task_action.TaskAction,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_fail_create.param_model.TasksFailCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_action.TaskAction:
        import gsmtasks.paths.tasks_fail_create.param_model

        param_model = gsmtasks.paths.tasks_fail_create.param_model.TasksFailCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/fail/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_list(
        self,
        *,
        q_account: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_account__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__apartment_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__city__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__country_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__formatted_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocode_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__geocoded_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__google_place_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__house_number__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__point_of_interest__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__postal_code__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__raw_address__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__state__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address__street__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_data: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_address_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__email__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__first_name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__last_name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee__phone__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_proximity: typing.Union[
            gsmtasks.paths.tasks_list.param_model.TasksListAssigneeProximity,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_assignee_proximity__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_barcodes__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cancelled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_category: typing.Union[
            gsmtasks.paths.tasks_list.param_model.TasksListCategory,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_category__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_after__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_complete_before__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__company__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__email__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__name__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__notes__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phone__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_data: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_contact_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_by__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_description__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_external_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.tasks_list.param_model.TasksListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_id__in: typing.Union[
            list[
                uuid.UUID,
            ],
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_optimal: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_is_optimal__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__accepted_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__active_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__assigned_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__cancelled_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__completed_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__documents_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__events_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__failed_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_completed_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__forms_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_accepted_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_active_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_assigned_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_cancelled_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_completed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_failed_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_transit_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__last_unassigned_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__signatures_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__task_event_notes_count__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__transit_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_distance__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metadata__unassigned_duration__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_metafields__namespace_key: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__auto_assign: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__created_by__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__external_id__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__reference__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_orderer_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_owner_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_position__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_previous_assignees__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_priority__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_receiver_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__iregex: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_reference__search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_route_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_scheduled_time__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__isnull: typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_size__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.tasks_list.param_model.TasksListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state__not_in_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task_import: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task_import__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_unassignee_id__isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_sideload: typing.Union[
            list[
                gsmtasks.paths.tasks_list.param_model.TasksListSideloadItem,
            ],
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        list[
            gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
        ],
        gsmtasks.components.schemas.task_list_ext.TaskListExt,
    ]:
        import gsmtasks.paths.tasks_list.param_model

        param_model = gsmtasks.paths.tasks_list.param_model.TasksList(**locals())
        return await super()._request(
            "GET",
            f"/tasks/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        list[
                            gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2
                        ],
                        gsmtasks.components.schemas.task_list_ext.TaskListExt,
                    ],
                    "application/xml; version=2.4.11": list[
                        gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_task_serializer_v2.PatchedTaskSerializerV2,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_partial_update.param_model.TasksPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2:
        import gsmtasks.paths.tasks_partial_update.param_model

        param_model = (
            gsmtasks.paths.tasks_partial_update.param_model.TasksPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/tasks/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_reject_create(
        self,
        request_body: gsmtasks.components.schemas.task_action.TaskAction,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_reject_create.param_model.TasksRejectCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_action.TaskAction:
        import gsmtasks.paths.tasks_reject_create.param_model

        param_model = gsmtasks.paths.tasks_reject_create.param_model.TasksRejectCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/reject/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_reorder_create(
        self,
        request_body: gsmtasks.components.schemas.task_list_reorder_request.TaskListReorderRequest,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.tasks_reorder_create.param_model.TasksReorderCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_list_reorder_request.TaskListReorderRequest:
        import gsmtasks.paths.tasks_reorder_create.param_model

        param_model = (
            gsmtasks.paths.tasks_reorder_create.param_model.TasksReorderCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/tasks/reorder/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_list_reorder_request.TaskListReorderRequest,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_list_reorder_request.TaskListReorderRequest,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_reposition_create(
        self,
        request_body: gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.tasks_reposition_create.param_model.TasksRepositionCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2:
        import gsmtasks.paths.tasks_reposition_create.param_model

        param_model = (
            gsmtasks.paths.tasks_reposition_create.param_model.TasksRepositionCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/tasks/reposition/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_retrieve.param_model.TasksRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2:
        import gsmtasks.paths.tasks_retrieve.param_model

        param_model = gsmtasks.paths.tasks_retrieve.param_model.TasksRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/tasks/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_signatures_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_signatures_retrieve.param_model.TasksSignaturesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2:
        import gsmtasks.paths.tasks_signatures_retrieve.param_model

        param_model = gsmtasks.paths.tasks_signatures_retrieve.param_model.TasksSignaturesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/tasks/{p_id}/signatures/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_transit_create(
        self,
        request_body: gsmtasks.components.schemas.task_action.TaskAction,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_transit_create.param_model.TasksTransitCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_action.TaskAction:
        import gsmtasks.paths.tasks_transit_create.param_model

        param_model = (
            gsmtasks.paths.tasks_transit_create.param_model.TasksTransitCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/transit/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_unaccept_create(
        self,
        request_body: gsmtasks.components.schemas.task_action.TaskAction,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_unaccept_create.param_model.TasksUnacceptCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_action.TaskAction:
        import gsmtasks.paths.tasks_unaccept_create.param_model

        param_model = (
            gsmtasks.paths.tasks_unaccept_create.param_model.TasksUnacceptCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/unaccept/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_unassign_create(
        self,
        request_body: gsmtasks.components.schemas.task_action.TaskAction,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_unassign_create.param_model.TasksUnassignCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_action.TaskAction:
        import gsmtasks.paths.tasks_unassign_create.param_model

        param_model = (
            gsmtasks.paths.tasks_unassign_create.param_model.TasksUnassignCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/tasks/{p_id}/unassign/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_action.TaskAction,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def tasks_update(
        self,
        request_body: gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.tasks_update.param_model.TasksUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__company__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__emails__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__name__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__icontains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__iexact: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__notes__istartswith: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contained_by: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__contains: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_order__orderer__phones__overlap: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2:
        import gsmtasks.paths.tasks_update.param_model

        param_model = gsmtasks.paths.tasks_update.param_model.TasksUpdate(**locals())
        return await super()._request(
            "PUT",
            f"/tasks/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                    "application/xml; version=2.4.11": gsmtasks.components.schemas.task_serializer_v2.TaskSerializerV2,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def time_location_features_create(
        self,
        request_body: gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.time_location_features_create.param_model.TimeLocationFeaturesCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.time_location_feature.TimeLocationFeature:
        import gsmtasks.paths.time_location_features_create.param_model

        param_model = gsmtasks.paths.time_location_features_create.param_model.TimeLocationFeaturesCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/time_location_features/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def time_location_features_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.time_location_features_destroy.param_model.TimeLocationFeaturesDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.time_location_features_destroy.param_model

        param_model = gsmtasks.paths.time_location_features_destroy.param_model.TimeLocationFeaturesDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/time_location_features/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def time_location_features_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.time_location_features_list.param_model.TimeLocationFeaturesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.time_location_features_list.param_model.TimeLocationFeaturesListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,]:
        import gsmtasks.paths.time_location_features_list.param_model

        param_model = gsmtasks.paths.time_location_features_list.param_model.TimeLocationFeaturesList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/time_location_features/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.time_location_feature.TimeLocationFeature
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.time_location_feature.TimeLocationFeature
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def time_location_features_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_time_location_feature.PatchedTimeLocationFeature,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.time_location_features_partial_update.param_model.TimeLocationFeaturesPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.time_location_feature.TimeLocationFeature:
        import gsmtasks.paths.time_location_features_partial_update.param_model

        param_model = gsmtasks.paths.time_location_features_partial_update.param_model.TimeLocationFeaturesPartialUpdate(
            **locals()
        )
        return await super()._request(
            "PATCH",
            f"/time_location_features/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def time_location_features_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.time_location_features_retrieve.param_model.TimeLocationFeaturesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.time_location_feature.TimeLocationFeature:
        import gsmtasks.paths.time_location_features_retrieve.param_model

        param_model = gsmtasks.paths.time_location_features_retrieve.param_model.TimeLocationFeaturesRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/time_location_features/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def time_location_features_update(
        self,
        request_body: gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.time_location_features_update.param_model.TimeLocationFeaturesUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.time_location_feature.TimeLocationFeature:
        import gsmtasks.paths.time_location_features_update.param_model

        param_model = gsmtasks.paths.time_location_features_update.param_model.TimeLocationFeaturesUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/time_location_features/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.time_location_feature.TimeLocationFeature,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def time_locations_create(
        self,
        request_body: gsmtasks.components.schemas.time_location.TimeLocation,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.time_locations_create.param_model.TimeLocationsCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.time_location.TimeLocation:
        import gsmtasks.paths.time_locations_create.param_model

        param_model = (
            gsmtasks.paths.time_locations_create.param_model.TimeLocationsCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/time_locations/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.time_location.TimeLocation,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.time_location.TimeLocation,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def time_locations_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.time_locations_list.param_model.TimeLocationsListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.time_locations_list.param_model.TimeLocationsListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.time_location.TimeLocation,]:
        import gsmtasks.paths.time_locations_list.param_model

        param_model = gsmtasks.paths.time_locations_list.param_model.TimeLocationsList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/time_locations/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.time_location.TimeLocation
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.time_location.TimeLocation
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def time_locations_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.time_locations_retrieve.param_model.TimeLocationsRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.time_location.TimeLocation:
        import gsmtasks.paths.time_locations_retrieve.param_model

        param_model = (
            gsmtasks.paths.time_locations_retrieve.param_model.TimeLocationsRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/time_locations/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.time_location.TimeLocation,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.time_location.TimeLocation,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def trackers_create(
        self,
        request_body: gsmtasks.components.schemas.tracker.Tracker,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.trackers_create.param_model.TrackersCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.tracker.Tracker:
        import gsmtasks.paths.trackers_create.param_model

        param_model = gsmtasks.paths.trackers_create.param_model.TrackersCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/trackers/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def trackers_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.trackers_list.param_model.TrackersListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.tracker.Tracker,]:
        import gsmtasks.paths.trackers_list.param_model

        param_model = gsmtasks.paths.trackers_list.param_model.TrackersList(**locals())
        return await super()._request(
            "GET",
            f"/trackers/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.tracker.Tracker
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.tracker.Tracker
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def trackers_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_tracker.PatchedTracker,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.trackers_partial_update.param_model.TrackersPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.tracker.Tracker:
        import gsmtasks.paths.trackers_partial_update.param_model

        param_model = (
            gsmtasks.paths.trackers_partial_update.param_model.TrackersPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/trackers/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def trackers_public_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.trackers_public_retrieve.param_model.TrackersPublicRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.tracker.Tracker:
        import gsmtasks.paths.trackers_public_retrieve.param_model

        param_model = (
            gsmtasks.paths.trackers_public_retrieve.param_model.TrackersPublicRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/trackers/{p_id}/public/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def trackers_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.trackers_retrieve.param_model.TrackersRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.tracker.Tracker:
        import gsmtasks.paths.trackers_retrieve.param_model

        param_model = gsmtasks.paths.trackers_retrieve.param_model.TrackersRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/trackers/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def trackers_update(
        self,
        request_body: gsmtasks.components.schemas.tracker.Tracker,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.trackers_update.param_model.TrackersUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.tracker.Tracker:
        import gsmtasks.paths.trackers_update.param_model

        param_model = gsmtasks.paths.trackers_update.param_model.TrackersUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/trackers/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.tracker.Tracker,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_activate_create(
        self,
        request_body: gsmtasks.components.schemas.user_activation.UserActivation,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.users_activate_create.param_model.UsersActivateCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.on_duty.OnDuty,
        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        gsmtasks.components.schemas.readable_user.ReadableUser,
    ]:
        import gsmtasks.paths.users_activate_create.param_model

        param_model = (
            gsmtasks.paths.users_activate_create.param_model.UsersActivateCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/users/{p_id}/activate/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                    "application/xml; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_create(
        self,
        request_body: gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.users_create.param_model.UsersCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.on_duty.OnDuty,
        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        gsmtasks.components.schemas.readable_user.ReadableUser,
    ]:
        import gsmtasks.paths.users_create.param_model

        param_model = gsmtasks.paths.users_create.param_model.UsersCreate(**locals())
        return await super()._request(
            "POST",
            f"/users/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                    "application/xml; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.users_destroy.param_model.UsersDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.on_duty.OnDuty,
        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        gsmtasks.components.schemas.readable_user.ReadableUser,
    ]:
        import gsmtasks.paths.users_destroy.param_model

        param_model = gsmtasks.paths.users_destroy.param_model.UsersDestroy(**locals())
        return await super()._request(
            "DELETE",
            f"/users/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                    "application/xml; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_list(
        self,
        *,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.users_list.param_model.UsersListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[
        typing.Union[
            gsmtasks.components.schemas.on_duty.OnDuty,
            gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
            gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
            gsmtasks.components.schemas.readable_user.ReadableUser,
        ],
    ]:
        import gsmtasks.paths.users_list.param_model

        param_model = gsmtasks.paths.users_list.param_model.UsersList(**locals())
        return await super()._request(
            "GET",
            f"/users/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        typing.Union[
                            gsmtasks.components.schemas.on_duty.OnDuty,
                            gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                            gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                            gsmtasks.components.schemas.readable_user.ReadableUser,
                        ]
                    ],
                    "application/xml; version=2.4.11": list[
                        typing.Union[
                            gsmtasks.components.schemas.on_duty.OnDuty,
                            gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                            gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                            gsmtasks.components.schemas.readable_user.ReadableUser,
                        ]
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_on_duty_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.users_on_duty_destroy.param_model.UsersOnDutyDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.on_duty.OnDuty,
        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        gsmtasks.components.schemas.readable_user.ReadableUser,
    ]:
        import gsmtasks.paths.users_on_duty_destroy.param_model

        param_model = (
            gsmtasks.paths.users_on_duty_destroy.param_model.UsersOnDutyDestroy(
                **locals()
            )
        )
        return await super()._request(
            "DELETE",
            f"/users/{p_id}/on_duty/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                    "application/xml; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_on_duty_log_create(
        self,
        request_body: gsmtasks.components.schemas.working_state.WorkingState,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.users_on_duty_log_create.param_model.UsersOnDutyLogCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.working_state.WorkingState:
        import gsmtasks.paths.users_on_duty_log_create.param_model

        param_model = (
            gsmtasks.paths.users_on_duty_log_create.param_model.UsersOnDutyLogCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/users_on_duty_log/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.working_state.WorkingState,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.working_state.WorkingState,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_on_duty_log_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_account_role: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.users_on_duty_log_list.param_model.UsersOnDutyLogListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_mode: typing.Union[
            gsmtasks.paths.users_on_duty_log_list.param_model.UsersOnDutyLogListMode,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_status: typing.Union[
            gsmtasks.paths.users_on_duty_log_list.param_model.UsersOnDutyLogListStatus,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.working_state.WorkingState,]:
        import gsmtasks.paths.users_on_duty_log_list.param_model

        param_model = (
            gsmtasks.paths.users_on_duty_log_list.param_model.UsersOnDutyLogList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/users_on_duty_log/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.working_state.WorkingState
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.working_state.WorkingState
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_on_duty_log_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.users_on_duty_log_retrieve.param_model.UsersOnDutyLogRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.working_state.WorkingState:
        import gsmtasks.paths.users_on_duty_log_retrieve.param_model

        param_model = gsmtasks.paths.users_on_duty_log_retrieve.param_model.UsersOnDutyLogRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/users_on_duty_log/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.working_state.WorkingState,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.working_state.WorkingState,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_on_duty_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.users_on_duty_retrieve.param_model.UsersOnDutyRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.on_duty.OnDuty,
        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        gsmtasks.components.schemas.readable_user.ReadableUser,
    ]:
        import gsmtasks.paths.users_on_duty_retrieve.param_model

        param_model = (
            gsmtasks.paths.users_on_duty_retrieve.param_model.UsersOnDutyRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/users/{p_id}/on_duty/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                    "application/xml; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_on_duty_update(
        self,
        request_body: gsmtasks.components.schemas.on_duty.OnDuty,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.users_on_duty_update.param_model.UsersOnDutyUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.on_duty.OnDuty,
        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        gsmtasks.components.schemas.readable_user.ReadableUser,
    ]:
        import gsmtasks.paths.users_on_duty_update.param_model

        param_model = gsmtasks.paths.users_on_duty_update.param_model.UsersOnDutyUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/users/{p_id}/on_duty/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                    "application/xml; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_authenticated_user_update.PatchedAuthenticatedUserUpdate,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.users_partial_update.param_model.UsersPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.on_duty.OnDuty,
        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        gsmtasks.components.schemas.readable_user.ReadableUser,
    ]:
        import gsmtasks.paths.users_partial_update.param_model

        param_model = (
            gsmtasks.paths.users_partial_update.param_model.UsersPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/users/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                    "application/xml; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.users_retrieve.param_model.UsersRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.on_duty.OnDuty,
        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        gsmtasks.components.schemas.readable_user.ReadableUser,
    ]:
        import gsmtasks.paths.users_retrieve.param_model

        param_model = gsmtasks.paths.users_retrieve.param_model.UsersRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/users/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                    "application/xml; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def users_update(
        self,
        request_body: gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.users_update.param_model.UsersUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> typing.Union[
        gsmtasks.components.schemas.on_duty.OnDuty,
        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
        gsmtasks.components.schemas.readable_user.ReadableUser,
    ]:
        import gsmtasks.paths.users_update.param_model

        param_model = gsmtasks.paths.users_update.param_model.UsersUpdate(**locals())
        return await super()._request(
            "PUT",
            f"/users/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                    "application/xml; version=2.4.11": typing.Union[
                        gsmtasks.components.schemas.on_duty.OnDuty,
                        gsmtasks.components.schemas.authenticated_user_create.AuthenticatedUserCreate,
                        gsmtasks.components.schemas.authenticated_user_update.AuthenticatedUserUpdate,
                        gsmtasks.components.schemas.readable_user.ReadableUser,
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def webhooks_active_create(
        self,
        request_body: gsmtasks.components.schemas.webhook.Webhook,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.webhooks_active_create.param_model.WebhooksActiveCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.webhook.Webhook:
        import gsmtasks.paths.webhooks_active_create.param_model

        param_model = (
            gsmtasks.paths.webhooks_active_create.param_model.WebhooksActiveCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/webhooks/{p_id}/active/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def webhooks_create(
        self,
        request_body: gsmtasks.components.schemas.webhook.Webhook,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.webhooks_create.param_model.WebhooksCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.webhook.Webhook:
        import gsmtasks.paths.webhooks_create.param_model

        param_model = gsmtasks.paths.webhooks_create.param_model.WebhooksCreate(
            **locals()
        )
        return await super()._request(
            "POST",
            f"/webhooks/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def webhooks_destroy(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.webhooks_destroy.param_model.WebhooksDestroyFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> None:
        import gsmtasks.paths.webhooks_destroy.param_model

        param_model = gsmtasks.paths.webhooks_destroy.param_model.WebhooksDestroy(
            **locals()
        )
        return await super()._request(
            "DELETE",
            f"/webhooks/{p_id}/",
            param_model=param_model,
            auth=self.auth_tokenAuth,
        )

    async def webhooks_inactive_create(
        self,
        request_body: gsmtasks.components.schemas.webhook.Webhook,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.webhooks_inactive_create.param_model.WebhooksInactiveCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.webhook.Webhook:
        import gsmtasks.paths.webhooks_inactive_create.param_model

        param_model = (
            gsmtasks.paths.webhooks_inactive_create.param_model.WebhooksInactiveCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/webhooks/{p_id}/inactive/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def webhooks_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_document_events: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.webhooks_list.param_model.WebhooksListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_review_events: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_search: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_signature_events: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.webhooks_list.param_model.WebhooksListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_task_events: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_version: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.webhook.Webhook,]:
        import gsmtasks.paths.webhooks_list.param_model

        param_model = gsmtasks.paths.webhooks_list.param_model.WebhooksList(**locals())
        return await super()._request(
            "GET",
            f"/webhooks/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.webhook.Webhook
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.webhook.Webhook
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def webhooks_partial_update(
        self,
        request_body: gsmtasks.components.schemas.patched_webhook.PatchedWebhook,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.webhooks_partial_update.param_model.WebhooksPartialUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.webhook.Webhook:
        import gsmtasks.paths.webhooks_partial_update.param_model

        param_model = (
            gsmtasks.paths.webhooks_partial_update.param_model.WebhooksPartialUpdate(
                **locals()
            )
        )
        return await super()._request(
            "PATCH",
            f"/webhooks/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def webhooks_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.webhooks_retrieve.param_model.WebhooksRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.webhook.Webhook:
        import gsmtasks.paths.webhooks_retrieve.param_model

        param_model = gsmtasks.paths.webhooks_retrieve.param_model.WebhooksRetrieve(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/webhooks/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def webhooks_update(
        self,
        request_body: gsmtasks.components.schemas.webhook.Webhook,
        /,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.webhooks_update.param_model.WebhooksUpdateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.webhook.Webhook:
        import gsmtasks.paths.webhooks_update.param_model

        param_model = gsmtasks.paths.webhooks_update.param_model.WebhooksUpdate(
            **locals()
        )
        return await super()._request(
            "PUT",
            f"/webhooks/{p_id}/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.webhook.Webhook,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def worker_features_list(
        self,
        *,
        q_account: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_account__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.worker_features_list.param_model.WorkerFeaturesListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_state: typing.Union[
            gsmtasks.paths.worker_features_list.param_model.WorkerFeaturesListState,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_time__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user__in: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.worker_feature.WorkerFeature,]:
        import gsmtasks.paths.worker_features_list.param_model

        param_model = (
            gsmtasks.paths.worker_features_list.param_model.WorkerFeaturesList(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/worker_features/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.worker_feature.WorkerFeature
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.worker_feature.WorkerFeature
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def worker_features_retrieve(
        self,
        *,
        p_user_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.worker_features_retrieve.param_model.WorkerFeaturesRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.worker_feature.WorkerFeature:
        import gsmtasks.paths.worker_features_retrieve.param_model

        param_model = (
            gsmtasks.paths.worker_features_retrieve.param_model.WorkerFeaturesRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/worker_features/{p_user_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.worker_feature.WorkerFeature,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.worker_feature.WorkerFeature,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def worker_tracks_list(
        self,
        *,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_end_time__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.worker_tracks_list.param_model.WorkerTracksListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_start_time__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_updated_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.worker_track.WorkerTrack,]:
        import gsmtasks.paths.worker_tracks_list.param_model

        param_model = gsmtasks.paths.worker_tracks_list.param_model.WorkerTracksList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/worker_tracks/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.worker_track.WorkerTrack
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.worker_track.WorkerTrack
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def working_state_create(
        self,
        request_body: gsmtasks.components.schemas.working_state.WorkingState,
        /,
        *,
        q_format: typing.Union[
            gsmtasks.paths.working_state_create.param_model.WorkingStateCreateFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.working_state.WorkingState:
        import gsmtasks.paths.working_state_create.param_model

        param_model = (
            gsmtasks.paths.working_state_create.param_model.WorkingStateCreate(
                **locals()
            )
        )
        return await super()._request(
            "POST",
            f"/working_state/",
            param_model=param_model,
            request_body=request_body,
            response_map={
                "201": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.working_state.WorkingState,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.working_state.WorkingState,
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def working_state_list(
        self,
        *,
        q_account: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_account_role: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_created_at__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_cursor: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_format: typing.Union[
            gsmtasks.paths.working_state_list.param_model.WorkingStateListFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_mode: typing.Union[
            gsmtasks.paths.working_state_list.param_model.WorkingStateListMode,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_ordering: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_page_size: typing.Union[
            int,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_status: typing.Union[
            gsmtasks.paths.working_state_list.param_model.WorkingStateListStatus,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__date: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__date_or_isnull: typing.Union[
            datetime.date,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__gt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__gt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__gte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__gte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__lt: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__lt_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__lte: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_timestamp__lte_or_isnull: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
        q_user: typing.Union[
            str,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> list[gsmtasks.components.schemas.working_state.WorkingState,]:
        import gsmtasks.paths.working_state_list.param_model

        param_model = gsmtasks.paths.working_state_list.param_model.WorkingStateList(
            **locals()
        )
        return await super()._request(
            "GET",
            f"/working_state/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": list[
                        gsmtasks.components.schemas.working_state.WorkingState
                    ],
                    "application/xlsx; version=2.4.11": list[
                        gsmtasks.components.schemas.working_state.WorkingState
                    ],
                },
            },
            auth=self.auth_tokenAuth,
        )

    async def working_state_retrieve(
        self,
        *,
        p_id: uuid.UUID,
        q_format: typing.Union[
            gsmtasks.paths.working_state_retrieve.param_model.WorkingStateRetrieveFormat,
            lapidary_base.absent.Absent,
        ] = lapidary_base.absent.ABSENT,
    ) -> gsmtasks.components.schemas.working_state.WorkingState:
        import gsmtasks.paths.working_state_retrieve.param_model

        param_model = (
            gsmtasks.paths.working_state_retrieve.param_model.WorkingStateRetrieve(
                **locals()
            )
        )
        return await super()._request(
            "GET",
            f"/working_state/{p_id}/",
            param_model=param_model,
            response_map={
                "200": {
                    "application/json; version=2.4.11": gsmtasks.components.schemas.working_state.WorkingState,
                    "application/xlsx; version=2.4.11": gsmtasks.components.schemas.working_state.WorkingState,
                },
            },
            auth=self.auth_tokenAuth,
        )
