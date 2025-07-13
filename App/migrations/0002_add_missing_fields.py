# Generated manually to fix production database
from django.db import migrations, models
import django.core.validators

class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        # This migration will only run if the fields don't exist
        # It's safe to run multiple times
        migrations.RunSQL(
            """
            DO $$ 
            BEGIN
                -- Check if phoneNumber column exists, if not add it
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='App_profile' AND column_name='phoneNumber') THEN
                    ALTER TABLE "App_profile" ADD COLUMN "phoneNumber" varchar(17) DEFAULT ' ';
                END IF;
                
                -- Check if account_type column exists, if not add it
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='App_profile' AND column_name='account_type') THEN
                    ALTER TABLE "App_profile" ADD COLUMN "account_type" varchar(20) DEFAULT 'community';
                END IF;
                
                -- Check if donor_tier column exists, if not add it
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='App_profile' AND column_name='donor_tier') THEN
                    ALTER TABLE "App_profile" ADD COLUMN "donor_tier" varchar(20);
                END IF;
                
                -- Check if monthly_contribution column exists, if not add it
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='App_profile' AND column_name='monthly_contribution') THEN
                    ALTER TABLE "App_profile" ADD COLUMN "monthly_contribution" decimal(10,2) DEFAULT 0.00;
                END IF;
                
                -- Check if total_donated column exists, if not add it
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='App_profile' AND column_name='total_donated') THEN
                    ALTER TABLE "App_profile" ADD COLUMN "total_donated" decimal(10,2) DEFAULT 0.00;
                END IF;
                
                -- Check if donor_since column exists, if not add it
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='App_profile' AND column_name='donor_since') THEN
                    ALTER TABLE "App_profile" ADD COLUMN "donor_since" timestamp with time zone;
                END IF;
            END $$;
            """,
            reverse_sql="-- No reverse needed"
        ),
    ]