"""expand_god_messages_to_20

Revision ID: 04bf893ba1aa
Revises: 88a53fc8a1c4
Create Date: 2026-01-29 10:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text
import json


# revision identifiers, used by Alembic.
revision: str = '04bf893ba1aa'
down_revision: Union[str, Sequence[str], None] = '88a53fc8a1c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


GOD_MESSAGES = {
    "Athena": {
        "focus_messages": [
            "Channel your inner strategist. Every great victory begins with a focused mind.",
            "Wisdom comes to those who persist. Stay the course.",
            "Your mind is a temple. Guard it with focused intention.",
            "Strategy wins battles. Plan your approach and execute with precision.",
            "The owl sees in darkness what others cannot. Use your insight.",
            "A thousand small decisions lead to one great outcome. Focus on each step.",
            "Clarity of thought is your greatest weapon. Wield it wisely.",
            "The wise know when to think and when to act. Now is the time to act.",
            "Knowledge without application is wasted. Apply yourself fully.",
            "Every problem has a solution. Approach it methodically.",
            "Let reason guide your actions, not impulse.",
            "The greatest battles are won in the mind first.",
            "Patience and persistence conquer all obstacles.",
            "Your intellect is sharper than any sword. Cut through distractions.",
            "The path to wisdom is paved with focused effort.",
            "Think deeply, act decisively. You have the wisdom for both.",
            "A strategic mind never wastes energy on trivial matters.",
            "Focus is the lens through which brilliance shines.",
            "The disciplined mind achieves what others think impossible.",
            "Victory favors the prepared. You are ready."
        ],
        "break_messages": [
            "Even the wisest minds need rest. Reflect on what you've accomplished.",
            "Step back and see the bigger picture. Clarity comes in stillness.",
            "A strategic pause is not weakness—it's wisdom.",
            "Let your thoughts settle like dust after battle.",
            "Wisdom grows in moments of quiet reflection.",
            "Rest sharpens the mind like a whetstone sharpens a blade.",
            "The owl rests by day to see clearly by night.",
            "Pause and consider: what wisdom have you gained?",
            "A clear mind returns to battle stronger than before.",
            "Strategic retreat allows for greater advance.",
            "In stillness, the mind finds answers it missed in motion.",
            "Your mental reserves need replenishing. Rest well.",
            "The wise conserve their energy for what matters most.",
            "Reflection transforms experience into wisdom.",
            "A moment of peace brings hours of productivity.",
            "Let your accomplishments sink in. You've earned this pause.",
            "The mind, like a garden, needs fallow periods to flourish.",
            "Rest is the companion of sustained excellence.",
            "Take stock of your victories, however small.",
            "Wisdom knows the value of well-timed rest."
        ],
        "session_start_messages": [
            "The owl awakens. Let wisdom guide your focus.",
            "Strategy begins now. What will you conquer?",
            "Your mind is sharp. Let's put it to work.",
            "A new challenge awaits your strategic brilliance.",
            "The battlefield of productivity lies before you. Advance wisely.",
            "Clear your mind and sharpen your focus. We begin.",
            "Wisdom calls you to action. Answer with excellence.",
            "Every great achievement starts with a single focused moment.",
            "The temple of your mind opens. Enter with purpose.",
            "Strategy is your ally, focus your weapon. Begin.",
            "Let calculated determination guide your every action.",
            "The path of wisdom unfolds before you. Walk it with focus.",
            "Your potential awaits activation. Engage your full intellect.",
            "A wise approach yields wise results. Proceed thoughtfully.",
            "The goddess of wisdom watches over your efforts. Make them count.",
            "Mental clarity achieved. Objectives locked. Commence.",
            "Your strategic advantage: unwavering focus. Deploy it now.",
            "The pursuit of excellence begins with this moment.",
            "Align your thoughts, steady your purpose. Advance.",
            "Wisdom and will combined. You're ready to succeed."
        ]
    },
    "Apollo": {
        "focus_messages": [
            "Let your creativity shine! The muses are watching.",
            "Every stroke of genius begins with dedication. Create on!",
            "You are the artist of your own productivity. Paint boldly.",
            "Brilliance flows through those who stay committed.",
            "Your work is a masterpiece in progress. Keep creating.",
            "The sun never dims its light. Neither should your effort.",
            "Creativity and discipline dance together beautifully.",
            "Every moment of focus adds another ray to your brilliance.",
            "The arts require dedication. Pour your heart into this.",
            "Light up your work with the fire of inspiration.",
            "Your creative spirit grows stronger with each focused moment.",
            "Excellence in art comes from excellence in effort.",
            "The muses smile upon the dedicated. Keep going.",
            "Like the sun at noon, let your productivity peak.",
            "Each task is a note in your symphony of achievement.",
            "Radiance comes from within. Let your focus glow.",
            "Art and discipline are not opposites—they are partners.",
            "Your dedication makes the ordinary extraordinary.",
            "The creative path is walked one focused step at a time.",
            "Shine your light on this task. Transform it with your touch."
        ],
        "break_messages": [
            "Bask in the glow of your achievements. The sun applauds you!",
            "Rest your creative spirit. Inspiration awaits your return.",
            "Even the sun sets to rise again. Recharge your brilliance.",
            "Let the warmth of accomplishment wash over you.",
            "Your creative fires need tending. Rest and refuel.",
            "Inspiration gathers in moments of peaceful reflection.",
            "The arts celebrate those who know when to pause.",
            "Your light has shone brightly. Now let it rest.",
            "In the quiet, new melodies form. Listen for them.",
            "The sunset is just as beautiful as the sunrise. Enjoy this transition.",
            "Creativity blooms after periods of rest, like flowers after rain.",
            "Let the muses whisper while you recover your strength.",
            "Your artistic soul appreciates this moment of peace.",
            "Rest is the canvas upon which tomorrow's masterpiece will be painted.",
            "The golden hour of rest has arrived. Embrace it.",
            "Even Apollo's chariot pauses at day's end. Rest well.",
            "Let inspiration find you in this moment of stillness.",
            "Your creative well refills during these quiet moments.",
            "Beauty exists in rest as much as in action.",
            "The light within you recharges now. Feel it grow."
        ],
        "session_start_messages": [
            "The sun rises on your ambitions. Let there be light!",
            "Illuminate your tasks with creative fire!",
            "A new dawn, a new session. Shine bright!",
            "The muses gather. It's time to create something beautiful.",
            "Let your inner light guide this session to greatness.",
            "The golden hour of productivity begins now.",
            "Creativity meets discipline. Magic is about to happen.",
            "Rise like the morning sun—steady, bright, unstoppable.",
            "Your artistic journey continues. Paint this day with success.",
            "Apollo's chariot rides across the sky. Ride with it.",
            "Inspiration strikes. Capture it with focused action.",
            "The spotlight is on you. Time to perform brilliantly.",
            "Light, creativity, focus—all align for this moment.",
            "A new movement in your symphony begins now.",
            "The dawn of productivity breaks. Greet it with enthusiasm.",
            "Your creative powers are at their peak. Channel them well.",
            "Like sunlight through clouds, let your focus break through.",
            "The artistic path calls. Walk it with purpose.",
            "Illumination awaits those who seek it with focus.",
            "The day's masterpiece begins with this session."
        ]
    },
    "Ares": {
        "focus_messages": [
            "ATTACK your tasks! Show no mercy to procrastination!",
            "Warriors don't retreat. PUSH THROUGH!",
            "This is YOUR battlefield. Dominate it!",
            "CRUSH this task! Show no weakness!",
            "The flames of determination burn within you. UNLEASH THEM!",
            "Every obstacle is an enemy to be conquered. CHARGE!",
            "Your warrior spirit knows no limits. PROVE IT!",
            "Weakness is not an option. STRENGTH is your only path!",
            "Fight through the resistance! VICTORY awaits!",
            "Channel your inner warrior. This task WILL fall before you!",
            "The heat of battle forges the strongest warriors. Stay in the fire!",
            "Distractions are enemies at the gate. REPEL THEM!",
            "Your focus is a weapon. Strike with precision!",
            "ADVANCE! Every moment of focus is a battle won!",
            "The war drum beats. Match its rhythm with your productivity!",
            "Surrender is not in your vocabulary. FIGHT ON!",
            "Glory awaits those who push through pain. EARN IT!",
            "Your tasks tremble before your determination. GOOD!",
            "The battlefield respects only those who give their all. DO IT!",
            "CONQUER or be conquered. The choice is yours!"
        ],
        "break_messages": [
            "Even warriors rest between battles. Sharpen your blade.",
            "You've earned this respite, soldier. Stand down... for now.",
            "Recover your strength. The next battle awaits.",
            "The warrior who rests fights harder tomorrow.",
            "Catch your breath. The war isn't over, but this battle is won.",
            "Sharpen your weapons and rest your body. You'll need both.",
            "A brief retreat to advance further. Strategic rest.",
            "Your wounds heal, your strength returns. Rest well, warrior.",
            "The battlefield will wait. Recover your fury.",
            "Even Ares appreciates a moment to survey his victories.",
            "Rest is not weakness—it's preparation for greater battles.",
            "The fires dim for now. Let them rebuild their heat.",
            "You've fought well. Enjoy this hard-earned peace.",
            "Recharge your battle cry. The next charge approaches.",
            "Warriors need fuel. Rest and prepare for glory.",
            "The drums quiet. Let the silence restore your strength.",
            "Survey your conquered tasks. You've earned this moment.",
            "Rest like a warrior: ready to spring back into action.",
            "Your spirit remains unbroken. Let your body catch up.",
            "The lull before the storm. Use it wisely, warrior."
        ],
        "session_start_messages": [
            "TO BATTLE! Your tasks await their defeat!",
            "The drums of war thunder. CHARGE!",
            "Arm yourself with focus. Victory is near!",
            "The battlefield awaits your fury. ATTACK!",
            "Rise, warrior! Today we conquer!",
            "Steel your nerves and sharpen your mind. WAR!",
            "The cry of battle echoes. Answer it!",
            "No retreat, no surrender. ONLY VICTORY!",
            "Your enemies—distraction, procrastination—prepare to fall!",
            "The flames of war ignite. Burn through your tasks!",
            "CHARGE into this session like a warrior into battle!",
            "The taste of victory is near. FIGHT FOR IT!",
            "Your war cry sounds. Let productivity tremble!",
            "The gates of the fortress are open. STORM THEM!",
            "Rise from rest like a phoenix of fury. BEGIN!",
            "The battlefield is set. Show no mercy to your tasks!",
            "Ares watches. Make your god proud with your effort!",
            "Blood, sweat, determination—bring them all to this fight!",
            "The warrior spirit awakens. UNLEASH IT!",
            "Victory or nothing! The battle commences NOW!"
        ]
    },
    "Hephaestus": {
        "focus_messages": [
            "Every masterpiece is built one hammer strike at a time. Keep forging.",
            "The forge is hot. Let your work take shape.",
            "Patience and precision. You're crafting excellence.",
            "Great works require great patience. You have both.",
            "The anvil awaits your steady hand. Shape your success.",
            "Each detail matters in the forge of achievement.",
            "Craftsmanship is born from consistent, focused effort.",
            "The metal bends to your will. So will this task.",
            "Forge your destiny with every deliberate action.",
            "Quality over speed. Build something that lasts.",
            "The master craftsman works with calm determination.",
            "Your hands shape more than metal—they shape your future.",
            "In the forge of focus, raw potential becomes refined skill.",
            "Precision strikes yield precision results. Continue.",
            "The fire of creation burns steady. Feed it with focus.",
            "Every great creation began with patient, dedicated work.",
            "The craftsman's way: measure twice, cut once. Focus always.",
            "Your work ethic is your greatest tool. Wield it well.",
            "Building excellence requires building habits of focus.",
            "The forge respects those who respect the process."
        ],
        "break_messages": [
            "Set down your tools. Admire what you've built so far.",
            "Even the forge needs to cool. Rest your hands.",
            "Good craftsmanship requires stepping back to see your work.",
            "The metal cools, the craftsman rests. Both are necessary.",
            "Examine your progress with the eye of a master builder.",
            "Your tools need rest too. Set them aside briefly.",
            "The forge quiets. Appreciate the silence.",
            "Step back from the anvil. Let perspective return.",
            "Rest prepares the hands for finer work ahead.",
            "The craftsman's break is part of the craftsman's process.",
            "Cool your brow. The heat of creation is intense.",
            "Your work has taken shape. Admire its progress.",
            "Even Hephaestus pauses to evaluate his creations.",
            "Rest the body, sharpen the mind for the next task.",
            "The best creations come from rested, refreshed hands.",
            "Let the forge cool while you plan your next masterpiece.",
            "Quality rest produces quality work. Embrace it.",
            "Your creation awaits your return. It will still be there.",
            "The patient craftsman knows the value of timely breaks.",
            "Rest is not idleness—it's preparation for greater crafting."
        ],
        "session_start_messages": [
            "The forge fires up. What will you create today?",
            "Hammer in hand, let's build something great.",
            "The anvil awaits. Time to craft your success.",
            "The bellows breathe life into the forge. Begin your work.",
            "Ready your tools. A new creation awaits your skill.",
            "The craftsman returns to the forge. Let the work begin.",
            "Iron awaits transformation. So does this task.",
            "Light the forge fires. It's time to create.",
            "Your workshop is ready. Your skills are sharp. Begin.",
            "The master craftsman begins another masterpiece.",
            "From raw material to refined product. Start shaping.",
            "The forge glows with potential. Unlock it with focus.",
            "Your craft calls. Answer with dedicated hands.",
            "Time to add another creation to your legacy.",
            "The rhythmic work of building begins anew.",
            "Heat, hammer, determination—all are ready.",
            "The craftsman's day begins with a single strike.",
            "Your workspace awaits your transformative touch.",
            "Build something worthy of your skills today.",
            "The forge of productivity is lit. Get to work."
        ]
    },
    "Dionysus": {
        "focus_messages": [
            "Work hard now, and the celebration will be LEGENDARY!",
            "Even parties need planning. Focus now, dance later!",
            "The best celebrations are earned. Keep going!",
            "Think of the feast that awaits! Push through!",
            "The sweetest wine tastes sweeter after hard work!",
            "Every moment of focus brings the party closer!",
            "Joy multiplies when earned through effort!",
            "The grapes won't crush themselves! Get to work!",
            "Discipline now, revelry later. A perfect balance!",
            "Focus is the appetizer to celebration's main course!",
            "Your future self will thank you with a toast!",
            "The dance of productivity leads to the party of success!",
            "Earn your celebration with every focused minute!",
            "The best festivals follow the best efforts!",
            "Channel your party energy into this task!",
            "Productivity is just pre-celebration preparation!",
            "The harder you work, the sweeter the celebration!",
            "Let anticipation of joy fuel your focus!",
            "Work like there's a feast waiting at the finish line!",
            "The god of celebration endorses focused effort!"
        ],
        "break_messages": [
            "Time to celebrate! You've earned a moment of joy!",
            "The party has begun! Enjoy this well-deserved break!",
            "Raise a glass to yourself! You're doing amazing!",
            "The music plays for you! Dance into your break!",
            "Celebration mode: ACTIVATED! Enjoy every moment!",
            "You've earned this revelry! Let loose a little!",
            "The feast of rest is served! Dig in!",
            "Joy is your reward! Embrace it fully!",
            "Let the good vibes flow! You've earned them!",
            "The celebration committee approves this break!",
            "Toast to your accomplishments! They deserve recognition!",
            "Party like you've just conquered something—because you have!",
            "The sweet reward of rest after productive work!",
            "Let celebration replenish what effort depleted!",
            "Your spirit deserves this moment of pure joy!",
            "The grapes have become wine! Time to savor it!",
            "Revel in what you've achieved! You're magnificent!",
            "Break time is party time! Let the joy flow!",
            "Every achievement deserves a celebration. This is yours!",
            "Let happiness wash over you like a wave of wine!"
        ],
        "session_start_messages": [
            "Let's get this party started... with PRODUCTIVITY!",
            "The festivities begin with focus. Surprise!",
            "Ready to earn your celebration? Let's go!",
            "The best parties have productive preambles! Begin!",
            "Work now, party later—the eternal bargain! Accept it!",
            "Your celebration awaits at the end of this focus!",
            "The fun begins... with getting things done!",
            "Productivity party, table for one! Let's celebrate work!",
            "The road to revelry passes through focus-town!",
            "Time to work towards your next celebration!",
            "Every great party started with preparation! Start yours!",
            "The countdown to celebration begins with this session!",
            "Dionysus blesses those who earn their joy! Begin earning!",
            "The vineyard of productivity awaits your labor!",
            "Joy follows effort like music follows rhythm! Start!",
            "Your celebration is being prepared. Do your part!",
            "The sweetest parties await the hardest workers!",
            "Begin with focus, end with festivities!",
            "The god of wine approves this work session!",
            "Plant seeds of effort, harvest fruits of celebration!"
        ]
    }
}


def upgrade() -> None:
    """Update gods with expanded messages (20 per category)."""
    conn = op.get_bind()
    for god_name, messages in GOD_MESSAGES.items():
        conn.execute(
            text("""
                UPDATE gods
                SET focus_messages = :focus_messages,
                    break_messages = :break_messages,
                    session_start_messages = :session_start_messages
                WHERE name = :god_name
            """),
            {
                "focus_messages": json.dumps(messages["focus_messages"]),
                "break_messages": json.dumps(messages["break_messages"]),
                "session_start_messages": json.dumps(messages["session_start_messages"]),
                "god_name": god_name,
            }
        )


def downgrade() -> None:
    """Revert to original 3 messages per category."""
    ORIGINAL_MESSAGES = {
        "Athena": {
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
        "Apollo": {
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
        "Ares": {
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
        "Hephaestus": {
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
        "Dionysus": {
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
    }

    conn = op.get_bind()
    for god_name, messages in ORIGINAL_MESSAGES.items():
        conn.execute(
            text("""
                UPDATE gods
                SET focus_messages = :focus_messages,
                    break_messages = :break_messages,
                    session_start_messages = :session_start_messages
                WHERE name = :god_name
            """),
            {
                "focus_messages": json.dumps(messages["focus_messages"]),
                "break_messages": json.dumps(messages["break_messages"]),
                "session_start_messages": json.dumps(messages["session_start_messages"]),
                "god_name": god_name,
            }
        )
