import yaml
import os
import zoom

INCLUDE_MEETING_URLS = False


template = """
---
layout: paper
id: {id}
slides_live_id: 38915748
rocket_id: {rocket_id}
meeting_url: {meeting_url}
authors: "{authors}"
camera_ready: {camera_ready}
cmt_id: {cmt_id}
kind: {kind}
session_id: {session_id}
session_title: "{session_title}"
title: "{title}"
track: {track}
live: {live}
---
""".strip()


files = os.listdir("program")
for file in files:
	os.remove(os.path.join("program", file))


with open("_data/sessions.yml", "r") as fh:
	sessions = yaml.load(fh)

for session in sessions:
	for paper in session["papers"]:
		print(paper["id"])

		if INCLUDE_MEETING_URLS:
			meeting_id = "PML4DC2020_{}".format(paper["id"])
			try:
				meeting = zoom.read_json(meeting_id)
				paper["meeting_url"] = meeting["join_url"]
			except FileNotFoundError:
				print("No meeting '{}'".format(meeting_id))
				paper["meeting_url"] = ""
		else:
			paper["meeting_url"] = ""

		paper["camera_ready"] = str(paper["camera_ready"]).lower()
		paper["session_id"] = session["id"]
		paper["session_title"] = session["title"]
		paper["title"] = paper["title"].replace("\"", "\\\"")
		paper["rocket_id"] = "pml4dc2020_channel_{:02d}".format(paper["id"])
		paper["slides_live_id"] = paper["slides_live_id"]
		paper["live"] = "false"

		html = template.format(**paper)

		path = "program/pml4dc_{}.html".format(paper["id"])
		assert not os.path.exists(path)
		with open(path, "w") as fh:
			fh.write(html)


with open("_data/speakers.yml", "r") as fh:
	speakers = yaml.load(fh)

for speaker in speakers:
	print(speaker["id"])
	speaker["camera_ready"] = "false"
	speaker["session_id"] = 0
	speaker["session_title"] = speaker["kind"]
	speaker["title"] = speaker["title"].replace("\"", "\\\"")
	speaker["cmt_id"] = -1
	speaker["track"] = speaker["kind"]
	speaker["rocket_id"] = "pml4dc2020_channel_{:02d}".format(speaker["id"])
	#speaker["slides_live_id"] = speaker["slides_live_id"]
	speaker["live"] = str(speaker.get("live", False)).lower()
	speaker["meeting_url"] = ""

	html = template.format(**speaker)

	path = "program/pml4dc_{}.html".format(speaker["id"])
	assert not os.path.exists(path)
	with open(path, "w") as fh:
		fh.write(html)