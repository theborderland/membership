Just notes to be filled out for next year's team

# Ideas for next year
  * differentiate lottery memberships and invitaiton memberships, and make the invitaiton process different

# Before lottery registration
  * Determine location, price(s) and quotas (location: during xmas, ...)
  
  * Run logo competition
  * Make e-mail template design (before xmas)
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
  * update webpage (before xmas)
  * create facebook event (before xmas)
  * scale up container? (before xmas)
  * spam places: euroburners (jan 3), burners playground (done), (underbroen, labitat, other makerspaces and the boat)
  * email previous years' attendees, mailing list (jan 12-ish)


## webpage text
The Borderland is a community and an event that anyone can be part of. There are only participants, no volunteers, vendors, or organizers. Besides entry to the event, a membership gives you as much a say in what the event is as anyone else. 

Read more about the Borderland on [our website](https://theborderland.se).

Since capacity at the event is limited, we raffle off half of the memberships. The remaining memberships are sold by invitation. When you buy a membership you can invite someone.

Note that this sale is a bit different from previous years, particularly how transfers and invitations work.

### The Lottery

We conduct the sale in three stages:

  1. Lottery Registration
  
     You can [register](register/) to take part in the lottery until Wednesday January 29 16:00 Copenhagen time. 
     
  1. Lottery
  
     A few days after the registration deadline we raffle off half of the memberships. If you're picked you have two days to buy a membership, and you're guaranteed an invite that you can send to a friend.

  1. Invitation Sale
  
     Anyone who buys a membership can invite someone else, until we're sold out. It pays to be quick, because we send out invitations starting with the earliest one. You don't need to have registered in the lottery to be invited.

### More information
  * Memberships are personal, read about our [Secure Membership Exchange Programme (SMEP)](page/smep/)
  * Read the full [FAQ](page/faq/).

You can find our contact info in the FAQ.



## during registration
  * watch mailer-daemon delivery reports and track down people 
  * answer emails
  * periodic reminders of deadline
  


# End of lottery registration
  * update webpage (done)
  * Enable waiting list (done)
  
### webpage text

### The Lottery
...
We conduct the sale in three stages:

  1. Lottery Registration

  Registration is now closed.
     
  1. Lottery
  
    Very soon we'll raffle off half of the memberships. If you're picked you have two days to buy a membership, and you're guaranteed an invite that you can send to a friend.

  1. Invitation Sale
  
     Anyone who buys a membership can invite someone else, until we're sold out. It pays to be quick, because we send out invitations starting with the earliest one. You don't need to have registered in the lottery to be invited.
...

## Before any sales are done
  * edit pretix email texts (done 17 jan)
  * finish questionnaire (ish)
  * check that stripe is up to date (never done)
  * after that, generate and send vouchers to the board, they're guinea pigs (never done, they refused)
  

# Lottery
  * update webpage
  * Run the lottery draw (jan 31)
  * Run replication for board and lottery tags


# After lottery invitations expire
When there are so few lottery vouchers pending that they all get the chance to
+1, or they've all expired.
  * change invite q text. removed: 

          If you don't know who to invite yet you can: 
            1. Leave it empty and come back later (click the Edit button on your order), but if you wait for two days after the lottery draw there are no guarantees, or
            2. You can enter your own email address, but then if you won the lottery you will get invited straight away and the clock starts ticking.

          People who won the lottery go first, so if you were invited by someone your invite won't be sent until Sunday.

  * change birthdate descr.  removed: (02022020) 
        If you got your invitation through the lottery, your legal name and date of birth *must match* what you registered with. We will check. We also check ID at the port when you arrive.
  * Run replication for all voucher tags

<!-- we are here -->
# If we sell out too slowly
  * Send out more lottery invitations (implement voucher id reg update)
  * When lottery pool is exhausted, send out waiting list vouchers

# After sell-out
  * unhide products so they shown even without a voucher
  * update webpage
     
  * hide replication question
  * disable replication
  * move everyone invited without a voucher to waiting list
  * enable waiting list
  * enable refunds/SMEP
  * enable monster?
  
# before sending out tickets
  * disable changes (order modification deadline)
  * control names and dob against lottery vouchers
  * Upload ticket design
  * send out tickets

# Before the event
  * no sales at the gate
  * Prepare check in devices
  
