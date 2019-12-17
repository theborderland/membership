Just notes to be filled out for next year's team

# Before lottery registration
  * Determine location, price(s) and quotas
  
  * Run logo competition
  * Make e-mail template design
  * Design ticket
  
## Configure Pretix
  * (document the ones that should be set by plugin here)
  * Make sure waiting list is off
  * Disable automatic waiting list assignments (or use this feature?)
  * Number per order: 1
  * "This product can only be bought using a voucher."
  * Make sure refunds/SMEP is off
  * Make sure monster is off
  * set modification deadline to now, or before you run the check

## in the plugin
  * change deadline for registration
  * look for errant 2020s
  * update email texts
  
# Starting lottery registration
  * update webpage
  * create facebook event
  * spam places: euroburners, underbroen, labitat, other makerspaces and the boat
  * email previous years' attendees, mailing list  
  * scale up container?

# End of lottery registration
  * update webpage
  * Enable waiting list

## Before any sales are done
  * Upload ticket design
  * set modification deadline to now, or to before you run the check
  * edit pretix email texts
  * finish questionnaire
  * check that stripe is up to date
  * after that, generate and send vouchers to the board, they're guinea pigs 
  
# Lottery
  * update webpage
  * Run the lottery draw
  * Run replication for board and lottery tags

# After lottery invitations expire
When there are so few lottery vouchers pending that they all get the chance to
+1, or they've all expired.
  * Run replication for all voucher tags

# If we sell out too slowly
  * Send out more lottery invitations (implement voucher id reg update)
  * When lottery pool is exhausted, send out waiting list vouchers

# After sell-out
  * update webpage
  * hide replication question
  * disable replication
  * move everyone invited without a voucher to waiting list
  * enable waiting list
  * enable refunds/SMEP
  * enable monster

# Before the event
  * no sales at the gate
  * Prepare check in devices
  
