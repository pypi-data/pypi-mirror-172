
  !---------------------------------------------------------------------------! 
  ! strings: routines for dealing with strings                                ! 
  ! Implementations by: Pavlo O. Dral                                         !
  !---------------------------------------------------------------------------!

module strings
  implicit none

contains

function strUpper(str)
  implicit none
  ! Arguments
  character(len=*), intent(in) :: str
  ! Return value
  character(len=len(str)) :: strUpper
  ! Variables
  integer :: i

  do i=1,len(str)
    if(str(i:i) >= "a" .and. str(i:i) <= "z") then
      strUpper(i:i)=achar(iachar(str(i:i))-32)
    else
      strUpper(i:i)=str(i:i)
    endif
  end do
  
end function strUpper

end module strings
