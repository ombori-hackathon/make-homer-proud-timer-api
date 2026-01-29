"""seed_gods

Revision ID: 88a53fc8a1c4
Revises: 0c2331290a67
Create Date: 2026-01-29 09:37:56.187261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88a53fc8a1c4'
down_revision: Union[str, Sequence[str], None] = '0c2331290a67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    from sqlalchemy import table, column
    from sqlalchemy.dialects.postgresql import JSONB
    import sqlalchemy as sa

    gods = table(
        "gods",
        column("name", sa.String),
        column("domain", sa.String),
        column("icon", sa.String),
        column("coaching_style", sa.String),
        column("focus_messages", JSONB),
        column("break_messages", JSONB),
        column("session_start_messages", JSONB),
    )

    op.bulk_insert(
        gods,
        [
            {
                "name": "Athena",
                "domain": "Wisdom & Strategy",
                "icon": "brain.head.profile",
                "coaching_style": "Wise and measured, like a patient mentor guiding you through complexity",
                "focus_messages": [
                    "Channel your inner strategist. Every great victory begins with a focused mind.",
                    "Wisdom comes to those who persist. Stay the course.",
                    "Your mind is a temple. Guard it with focused intention."
                ],
                "break_messages": [
                    "Even the wisest minds need rest. Reflect on what you've accomplished.",
                    "Step back and see the bigger picture. Clarity comes in stillness.",
                    "A strategic pause is not weakness—it's wisdom."
                ],
                "session_start_messages": [
                    "The owl awakens. Let wisdom guide your focus.",
                    "Strategy begins now. What will you conquer?",
                    "Your mind is sharp. Let's put it to work."
                ]
            },
            {
                "name": "Apollo",
                "domain": "Arts & Light",
                "icon": "sun.max.fill",
                "coaching_style": "Artistic and inspiring, celebrating creativity and bringing light to dark corners",
                "focus_messages": [
                    "Let your creativity shine! The muses are watching.",
                    "Every stroke of genius begins with dedication. Create on!",
                    "You are the artist of your own productivity. Paint boldly."
                ],
                "break_messages": [
                    "Bask in the glow of your achievements. The sun applauds you!",
                    "Rest your creative spirit. Inspiration awaits your return.",
                    "Even the sun sets to rise again. Recharge your brilliance."
                ],
                "session_start_messages": [
                    "The sun rises on your ambitions. Let there be light!",
                    "Illuminate your tasks with creative fire!",
                    "A new dawn, a new session. Shine bright!"
                ]
            },
            {
                "name": "Ares",
                "domain": "War & Strength",
                "icon": "flame.fill",
                "coaching_style": "Aggressive and warrior-like, pushing you to conquer your tasks like battles",
                "focus_messages": [
                    "ATTACK your tasks! Show no mercy to procrastination!",
                    "Warriors don't retreat. PUSH THROUGH!",
                    "This is YOUR battlefield. Dominate it!"
                ],
                "break_messages": [
                    "Even warriors rest between battles. Sharpen your blade.",
                    "You've earned this respite, soldier. Stand down... for now.",
                    "Recover your strength. The next battle awaits."
                ],
                "session_start_messages": [
                    "TO BATTLE! Your tasks await their defeat!",
                    "The drums of war thunder. CHARGE!",
                    "Arm yourself with focus. Victory is near!"
                ]
            },
            {
                "name": "Hephaestus",
                "domain": "Forge & Craft",
                "icon": "hammer.fill",
                "coaching_style": "Patient craftsman energy, methodically building something great piece by piece",
                "focus_messages": [
                    "Every masterpiece is built one hammer strike at a time. Keep forging.",
                    "The forge is hot. Let your work take shape.",
                    "Patience and precision. You're crafting excellence."
                ],
                "break_messages": [
                    "Set down your tools. Admire what you've built so far.",
                    "Even the forge needs to cool. Rest your hands.",
                    "Good craftsmanship requires stepping back to see your work."
                ],
                "session_start_messages": [
                    "The forge fires up. What will you create today?",
                    "Hammer in hand, let's build something great.",
                    "The anvil awaits. Time to craft your success."
                ]
            },
            {
                "name": "Dionysus",
                "domain": "Wine & Celebration",
                "icon": "party.popper.fill",
                "coaching_style": "Playful and celebratory, making work feel like a party worth attending",
                "focus_messages": [
                    "Work hard now, and the celebration will be LEGENDARY!",
                    "Even parties need planning. Focus now, dance later!",
                    "The best celebrations are earned. Keep going!"
                ],
                "break_messages": [
                    "Time to celebrate! You've earned a moment of joy!",
                    "The party has begun! Enjoy this well-deserved break!",
                    "Raise a glass to yourself! You're doing amazing!"
                ],
                "session_start_messages": [
                    "Let's get this party started... with PRODUCTIVITY!",
                    "The festivities begin with focus. Surprise!",
                    "Ready to earn your celebration? Let's go!"
                ]
            }
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM gods WHERE name IN ('Athena', 'Apollo', 'Ares', 'Hephaestus', 'Dionysus')")
