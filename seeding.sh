#!/usr/bin/env bash
set -euo pipefail

# Seeds the Experience and Education tables with the entries currently
# hardcoded in index.html's "experience" section (COMPFEST 18 committee
# staff + Competitive Programming Teacher) plus the education history
# (MAN 2 Kota Malang + University of Indonesia). Safe to re-run: uses
# get_or_create on title/institution+program, so it won't create
# duplicates.
#
# Usage:
#   ./seed_experience.sh                # run from the project root (where manage.py lives)
#   MANAGE_PY=/path/to/manage.py ./seed_experience.sh

MANAGE_PY="${MANAGE_PY:-manage.py}"

if [ ! -f "$MANAGE_PY" ]; then
    echo "Error: could not find '$MANAGE_PY'. Run this from your Django project root," >&2
    echo "or set MANAGE_PY=/path/to/manage.py" >&2
    exit 1
fi

python "$MANAGE_PY" shell <<'PYEOF'
from datetime import datetime
from django.utils import timezone
from main.models import Experience, Education

def to_aware(dt):
    if dt is not None and timezone.is_naive(dt):
        return timezone.make_aware(dt)
    return dt

def seed(title, description, category, started_at, ended_at=None):
    obj, created = Experience.objects.get_or_create(
        title=title,
        defaults={"description": description, "category": category},
    )
    if not created:
        obj.description = description
        obj.category = category
        obj.save()

    # started_at uses auto_now_add=True, so it's ignored by .save()/.create().
    # A queryset .update() bypasses that and lets us set the real date.
    Experience.objects.filter(pk=obj.pk).update(
        started_at=to_aware(started_at),
        ended_at=to_aware(ended_at),
    )
    print(f"{'Created' if created else 'Updated'} experience: {title}")

def seed_education(institution, program, level, description, started_at, ended_at=None):
    obj, created = Education.objects.get_or_create(
        institution=institution,
        program=program,
        defaults={"description": description, "level": level},
    )
    if not created:
        obj.description = description
        obj.level = level
        obj.save()

    # started_at uses auto_now_add=True, same as Experience above.
    Education.objects.filter(pk=obj.pk).update(
        started_at=to_aware(started_at),
        ended_at=to_aware(ended_at),
    )
    print(f"{'Created' if created else 'Updated'} education: {institution}")

seed(
    title="Staff of General Committee - COMPFEST 18",
    description=(
        "Managed participant information and attendance while ensuring "
        "accurate and organized competition records. Facilitated "
        "communication between PICs, mentors, and judges, addressing "
        "operational issues and troubleshooting challenges during the "
        "event. Served as a Liaison Officer during the final round, "
        "coordinating on-site communication and supporting participants, "
        "mentors, and judges."
    ),
    category="volunteer",
    started_at=datetime(2026, 4, 1),
    ended_at=datetime(2026, 9, 1),
)

seed(
    title="Competitive Programming Teacher - Madrasah Aliyah Negeri 2 Kota Malang",
    description=(
        "Help students of Informatics Olympiad Club in Madrasah Aliyah "
        "Negeri 2 Kota Malang to learn competitive programming in "
        "preparation of National Olympiad in Informatics (Olimpiade Sains "
        "Nasional Bidang Informatika)"
    ),
    category="part-time",
    started_at=datetime(2025, 6, 1),
    ended_at=datetime(2026, 5, 1),
)

seed_education(
    institution="MAN 2 Kota Malang",
    program="Mathematics and Natural Science",
    level="high_school",
    description="Actively participating in Competitive Programming Club",
    started_at=datetime(2022, 7, 1),
    ended_at=datetime(2025, 4, 1),
)

seed_education(
    institution="University of Indonesia",
    program="Computer Science",
    level="undergraduate",
    description="Focusing on Data Science and Machine Learning",
    started_at=datetime(2025, 7, 1),
    ended_at=None,
)
PYEOF

echo "Seeding complete."