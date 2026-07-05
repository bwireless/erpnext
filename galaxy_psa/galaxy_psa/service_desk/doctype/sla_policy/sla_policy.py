from datetime import datetime, time, timedelta

from frappe.model.document import Document


class SLAPolicy(Document):
	def compute_targets(self, start: datetime) -> tuple[datetime, datetime]:
		"""Compute response and resolution deadlines from a ticket start time.

		Naive business-hours arithmetic — does not yet respect the linked
		Holiday List. Fill that in when we wire in Frappe's holiday utils.
		"""
		response = _add_business_hours(
			start, self.response_hours, self.business_hours_start, self.business_hours_end
		)
		resolution = _add_business_hours(
			start, self.resolution_hours, self.business_hours_start, self.business_hours_end
		)
		return response, resolution


def _add_business_hours(start: datetime, hours: float, day_start: time, day_end: time) -> datetime:
	day_len_h = (day_end.hour * 60 + day_end.minute - day_start.hour * 60 - day_start.minute) / 60.0
	if day_len_h <= 0:
		return start + timedelta(hours=hours)
	full_days, remainder_h = divmod(hours, day_len_h)
	target = start + timedelta(days=int(full_days), hours=remainder_h)
	# Clamp into business hours on the target day.
	if target.time() > day_end:
		target = datetime.combine(target.date() + timedelta(days=1), day_start) + timedelta(
			seconds=(target.time().hour * 3600 + target.time().minute * 60) - (day_end.hour * 3600 + day_end.minute * 60)
		)
	if target.time() < day_start:
		target = datetime.combine(target.date(), day_start)
	return target
